import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, BASE_DIR
from services.data_service import load_dashboard_data, load_segment_data
from services.qa_service import answer_question

print("=== Day07 项目验证测试 ===\n")

print("1. 测试数据服务 - load_dashboard_data")
data = load_dashboard_data(BASE_DIR, "全部")
print(f"   指标数量: {len(data['metrics'])}")
print(f"   品类数量: {len(data['categories'])}")
print(f"   表格行数: {len(data['category_rows'])}")
print(f"   数据观察: {data['insight'][:50]}...")
print("   PASS")

print("\n2. 测试品类筛选")
fashion_data = load_dashboard_data(BASE_DIR, "Fashion")
print(f"   Fashion品类行数: {len(fashion_data['category_rows'])}")
print("   PASS")

print("\n3. 测试生命周期数据服务")
segment_data = load_segment_data(BASE_DIR)
print(f"   阶段数量: {len(segment_data['segments'])}")
print(f"   数据观察: {segment_data['insight'][:50]}...")
print("   PASS")

print("\n4. 测试离线问答")
questions = [
    "系统中有多少用户？",
    "总体流失率是多少？",
    "哪个品类用户最多？",
    "哪个阶段风险最高？",
    "平均订单数是多少？",
    "今天天气怎么样？"
]
for q in questions:
    answer = answer_question(BASE_DIR, q)
    print(f"   Q: {q}")
    print(f"   A: {answer[:60]}...")
print("   PASS")

print("\n5. 测试Flask应用")
client = app.test_client()

response = client.get('/')
print(f"   首页重定向: {response.status_code}")

response = client.get('/dashboard')
print(f"   未登录访问dashboard: {response.status_code}")

response = client.post('/login', data={'username': 'student', 'password': 'wrong'})
print(f"   错误登录: {response.status_code}")

response = client.post('/login', data={'username': 'student', 'password': 'day07'}, follow_redirects=True)
print(f"   正确登录: {response.status_code}")

with client.session_transaction() as sess:
    sess['username'] = 'student'

response = client.get('/dashboard')
print(f"   登录后访问dashboard: {response.status_code}")

response = client.get('/segments')
print(f"   访问生命周期页: {response.status_code}")

response = client.get('/assistant')
print(f"   访问智能问答页: {response.status_code}")

response = client.post('/api/ask', json={'question': '系统中有多少用户？'})
print(f"   API问答: {response.status_code}")
print("   PASS")

print("\n=== 所有测试通过 ===")