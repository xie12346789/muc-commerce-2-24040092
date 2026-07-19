from pathlib import Path

import pandas as pd


def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"
    metrics_df = pd.read_csv(data_dir / "overall_metrics.csv", encoding="utf-8-sig")
    category_df = pd.read_csv(data_dir / "category_analysis.csv", encoding="utf-8-sig")
    segment_df = pd.read_csv(data_dir / "segment_analysis.csv", encoding="utf-8-sig")

    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    normalized = question.replace(" ", "").lower()

    if any(word in normalized for word in ["多少用户", "用户数", "总用户"]):
        return f"数据集中共有{int(metrics['用户数']):,}名用户。"

    if any(word in normalized for word in ["流失率", "流失情况"]):
        churn_rate = float(metrics["流失率"])
        churn_count = int(metrics["流失人数"])
        total_users = int(metrics["用户数"])
        return f"总体流失率为{churn_rate:.1%}，共有{churn_count:,}名用户流失（占总用户{total_users:,}人的{churn_rate:.1%}）。"

    if any(word in normalized for word in ["偏好品类", "哪个品类", "品类用户"]):
        top_category = category_df.loc[category_df["用户数"].idxmax()]
        return f"用户最多的品类是{top_category['PreferedOrderCat']}，共有{int(top_category['用户数']):,}名用户偏好该品类。"

    if any(word in normalized for word in ["生命周期", "哪个阶段", "风险最高"]):
        highest_risk = segment_df.loc[segment_df["流失率"].idxmax()]
        return f"生命周期风险最高的阶段是{highest_risk['TenureGroup']}，该阶段流失率为{highest_risk['流失率']:.1%}。"

    if any(word in normalized for word in ["平均订单数", "订单数", "订单情况"]):
        avg_orders = float(metrics["平均订单数"])
        median_orders = float(metrics["订单数中位数"])
        return f"平均订单数为{avg_orders:.2f}单/人，订单数中位数为{median_orders:.2f}单。"

    return (
        "抱歉，我暂时无法回答这个问题。请尝试以下问法："
        "1. '系统中有多少用户？'"
        "2. '总体流失率是多少？'"
        "3. '哪个品类用户最多？'"
        "4. '哪个阶段风险最高？'"
        "5. '平均订单数是多少？'"
    )