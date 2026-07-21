import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["ok"] is True
    assert data["service"] == "day08-flask-upgrade"


def test_login_success(client):
    response = client.post("/login", data={"username": "student", "password": "day07"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"数据看板" in response.data


def test_login_failure(client):
    response = client.post("/login", data={"username": "student", "password": "wrong"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"账号或密码错误" in response.data


def test_unauthenticated_access(client):
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"请先登录" in response.data


def test_metrics_api_authenticated(client):
    client.post("/login", data={"username": "student", "password": "day07"})
    response = client.get("/api/metrics")
    assert response.status_code == 200
    data = response.get_json()
    assert data["ok"] is True
    assert len(data["metrics"]) == 4


def test_categories_api_authenticated(client):
    client.post("/login", data={"username": "student", "password": "day07"})
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = response.get_json()
    assert data["ok"] is True
    assert data["category"] == "全部"


def test_categories_api_with_filter(client):
    client.post("/login", data={"username": "student", "password": "day07"})
    response = client.get("/api/categories?category=Fashion")
    assert response.status_code == 200
    data = response.get_json()
    assert data["ok"] is True
    assert data["category"] == "Fashion"
    assert len(data["rows"]) == 1


def test_ask_api_empty_question(client):
    client.post("/login", data={"username": "student", "password": "day07"})
    response = client.post("/api/ask", json={"question": ""})
    assert response.status_code == 400
    data = response.get_json()
    assert data["ok"] is False
    assert "error" in data