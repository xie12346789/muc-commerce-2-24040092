from pathlib import Path

import pandas as pd


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def load_dashboard_data(base_dir: Path, selected_category: str = "全部") -> dict:
    data_dir = base_dir / "data"
    metrics_df = _read_csv(data_dir / "overall_metrics.csv")
    category_df = _read_csv(data_dir / "category_analysis.csv")
    segment_df = _read_csv(data_dir / "segment_analysis.csv")

    metric_map = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    metrics = [
        {"label": "总用户数", "value": f"{int(metric_map['用户数']):,}", "note": "人"},
        {"label": "流失用户", "value": f"{int(metric_map['流失人数']):,}", "note": "人"},
        {"label": "总体流失率", "value": f"{metric_map['流失率']:.1%}", "note": ""},
        {"label": "平均订单数", "value": f"{metric_map['平均订单数']:.2f}", "note": "单/人"},
    ]

    categories = ["全部", *category_df["PreferedOrderCat"].tolist()]
    table_df = category_df.copy()

    if selected_category != "全部":
        table_df = table_df[table_df["PreferedOrderCat"] == selected_category]

    table_df = table_df.rename(
        columns={
            "PreferedOrderCat": "偏好品类",
            "用户数": "用户数",
            "流失率": "流失率",
            "平均订单数": "平均订单数",
        }
    )[["偏好品类", "用户数", "流失率", "平均订单数"]]
    table_df["流失率"] = table_df["流失率"].map(lambda value: f"{value:.1%}")
    table_df["平均订单数"] = table_df["平均订单数"].map(lambda value: f"{value:.2f}")

    highest_risk_segment = segment_df.loc[segment_df["流失率"].idxmax()]
    insight = (
        f"生命周期风险观察：{highest_risk_segment['TenureGroup']}阶段流失率最高（{highest_risk_segment['流失率']:.1%}，{int(highest_risk_segment['用户数'])}人），"
        f"建议重点关注该阶段用户的留存策略。注：该结论基于现有样本统计，不代表因果关系。"
    )

    return {
        "metrics": metrics,
        "categories": categories,
        "category_rows": table_df.to_dict("records"),
        "insight": insight,
    }


def load_segment_data(base_dir: Path) -> dict:
    data_dir = base_dir / "data"
    segment_df = _read_csv(data_dir / "segment_analysis.csv")

    segment_df = segment_df.rename(
        columns={
            "TenureGroup": "生命周期阶段",
            "用户数": "用户数",
            "流失人数": "流失人数",
            "流失率": "流失率",
            "平均订单数": "平均订单数",
            "平均返现": "平均返现",
            "平均距上次下单天数": "平均距上次下单天数",
        }
    )
    segment_df["流失率"] = segment_df["流失率"].map(lambda value: f"{value:.1%}")
    segment_df["平均订单数"] = segment_df["平均订单数"].map(lambda value: f"{value:.2f}")
    segment_df["平均返现"] = segment_df["平均返现"].map(lambda value: f"{value:.2f}")
    segment_df["平均距上次下单天数"] = segment_df["平均距上次下单天数"].map(lambda value: f"{value:.2f}")

    highest_risk = segment_df.loc[segment_df["流失率"].str.replace("%", "").astype(float).idxmax()]
    lowest_risk = segment_df.loc[segment_df["流失率"].str.replace("%", "").astype(float).idxmin()]

    segment_insight = (
        f"关键发现：{highest_risk['生命周期阶段']}阶段流失率最高（{highest_risk['流失率']}），"
        f"而{lowest_risk['生命周期阶段']}阶段流失率最低（{lowest_risk['流失率']}），"
        f"两者相差约{abs(float(highest_risk['流失率'].replace('%', '')) - float(lowest_risk['流失率'].replace('%', ''))):.1f}个百分点。"
    )

    return {
        "segments": segment_df.to_dict("records"),
        "insight": segment_insight,
    }