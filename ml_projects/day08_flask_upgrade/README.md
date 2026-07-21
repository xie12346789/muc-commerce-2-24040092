# 第8天学生项目：Flask数据看板强化

## 运行方法

```bash
python -m pip install -r requirements.txt
python app.py
```

浏览器访问 `http://127.0.0.1:5500`。

- 用户名：`student`
- 密码：`day07`

## 学生信息

- 姓名：谢xx
- 学号：24040092
- 已完成路由或接口：/api/metrics、/api/categories、/health、统一400错误
- 测试文件：tests/test_app.py（8条测试用例）
- 尚未解决的问题：无

## API接口说明

### GET /api/metrics
返回四张指标卡的JSON数据
```json
{
    "ok": true,
    "metrics": [
        {"label": "总用户数", "value": "5,630", "note": "人"},
        {"label": "流失用户", "value": "948", "note": "人"},
        {"label": "总体流失率", "value": "16.8%", "note": "用户占比"},
        {"label": "平均订单数", "value": "2.96", "note": "单/人"}
    ]
}
```

### GET /api/categories?category=Fashion
返回筛选后的品类数据
```json
{
    "ok": true,
    "category": "Fashion",
    "rows": [{"偏好品类": "Fashion", "用户数": 826, "流失率": "15.5%", "平均订单数": "3.87"}]
}
```

### GET /health
健康检查接口（无需登录）
```json
{"ok": true, "service": "day08-flask-upgrade"}
```

### POST /api/ask
智能问答接口
```json
{
    "ok": true,
    "answer": "数据集中共有5,630名用户。"
}
```

## 测试运行

```bash
pip install pytest
pytest tests/test_app.py -v
```

## 核心TODO完成情况

- ✓ TODO 8-1：完成/api/metrics指标JSON接口
- ✓ TODO 8-2：完成/api/categories的查询参数筛选
- ✓ TODO 8-3：统一400错误JSON结构
- ✓ TODO 8-4：检查数据服务返回值可被jsonify序列化
- ✓ 为新增接口编写至少3条Flask测试（实际编写8条）