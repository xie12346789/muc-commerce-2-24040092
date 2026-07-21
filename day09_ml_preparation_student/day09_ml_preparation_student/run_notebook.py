from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data/ecommerce_customer_cleaned.csv"
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RANDOM_STATE = 42
TEST_SIZE = 0.20

STUDENT_NAME = "谢xx"
STUDENT_ID = "24040092"
CLASS_NAME = "电商数据分析"

print("任务1：人工规则演示")
toy = pd.DataFrame({
    "用户": list("ABCDEF"),
    "Tenure": [1, 24, 3, 18, 2, 30],
    "Complain": [1, 0, 0, 1, 1, 0],
    "Churn": [1, 0, 1, 0, 1, 0],
})
toy["人工规则预测"] = ((toy["Tenure"] <= 3) & (toy["Complain"] == 1)).astype(int)
toy["是否判断正确"] = toy["人工规则预测"] == toy["Churn"]
print(toy)
print("判断正确：", int(toy["是否判断正确"].sum()), "/", len(toy))

print("\n任务2：读取数据")
df = pd.read_csv(DATA_PATH)
print("数据形状：", df.shape)
print("总体流失率：", f"{df['Churn'].mean():.2%}")

print("\n任务3：建立X和y")
TARGET = "Churn"
ID_COL = "CustomerID"
X = df.drop(columns=[TARGET, ID_COL]).copy()
y = df[TARGET].astype(int).copy()
print("特征表：", X.shape, "标签：", y.shape)

print("\n任务4：特征方案")
categorical_features = X.select_dtypes(include="object").columns.tolist()
numeric_features = X.select_dtypes(exclude="object").columns.tolist()
derived_features = ["TenureGroup", "IsMobileLogin"]

rows = []
for column in df.columns:
    if column == ID_COL:
        role, action, reason = "identifier", "drop", "用户编号只用于追踪"
    elif column == TARGET:
        role, action, reason = "target", "separate", "这是希望预测的答案"
    elif column in derived_features:
        role, action, reason = "derived_feature", "candidate", "由已有字段转换得到"
    elif column in categorical_features:
        role, action, reason = "categorical_feature", "one_hot", "文字类别需要转成0/1列"
    else:
        role, action, reason = "numeric_feature", "numeric_pipeline", "进入教师提供的数值处理分支"
    rows.append({"feature": column, "role": role, "dtype": str(df[column].dtype), "action": action, "reason": reason})

feature_schema = pd.DataFrame(rows)
feature_schema.to_csv(OUTPUT_DIR / "feature_schema.csv", index=False, encoding="utf-8-sig")
print("已保存：feature_schema.csv")

print("\n任务5：数据划分")
STRATIFY_TARGET = y
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=STRATIFY_TARGET)

split_summary = pd.DataFrame([
    {"split": "train", "rows": len(X_train), "churn_count": int(y_train.sum()), "churn_rate": y_train.mean()},
    {"split": "test", "rows": len(X_test), "churn_count": int(y_test.sum()), "churn_rate": y_test.mean()},
])
split_summary.to_csv(OUTPUT_DIR / "split_summary.csv", index=False, encoding="utf-8-sig")
print("已保存：split_summary.csv")
print(split_summary)

print("\n任务6：预处理流水线")
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])
categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
])
preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, numeric_features),
    ("cat", categorical_pipeline, categorical_features),
])

X_train_ready = preprocessor.fit_transform(X_train)
X_test_ready = preprocessor.transform(X_test)
feature_names = preprocessor.get_feature_names_out()

model_matrix_preview = pd.DataFrame(X_train_ready[:20], columns=feature_names)
model_matrix_preview.to_csv(OUTPUT_DIR / "model_matrix_preview.csv", index=False, encoding="utf-8-sig")
print("训练矩阵：", X_train_ready.shape, "测试矩阵：", X_test_ready.shape)
print("已保存：model_matrix_preview.csv")

print("\n任务7：最低参照线")
baseline = DummyClassifier(strategy="prior", random_state=RANDOM_STATE)
baseline.fit(X_train_ready, y_train)
y_pred = baseline.predict(X_test_ready)

baseline_metrics = pd.DataFrame({
    "metric": ["accuracy", "churn_recall", "predicted_churn_count"],
    "value": [accuracy_score(y_test, y_pred), recall_score(y_test, y_pred, pos_label=1, zero_division=0), int(y_pred.sum())],
})
baseline_metrics.to_csv(OUTPUT_DIR / "baseline_metrics.csv", index=False, encoding="utf-8-sig")
print(baseline_metrics)
print("已保存：baseline_metrics.csv")
print("测试集中真实流失人数：", int(y_test.sum()))

print("\n任务8：解释")
reflection = "特征是用来预测的输入信息，如用户的使用月数和投诉记录；标签是要预测的目标答案，如用户是否流失。训练集是用来让模型学习规律的历史数据，测试集是用来评估模型效果的未知数据，两者必须分开才能避免过拟合。最低参照线是一个简单的基准模型，它永远预测最常见的类别，用来衡量正式模型是否有价值。如果正式模型的性能低于或接近最低参照线，说明模型没有学到有用的规律。"
print("解释字数：", len(reflection))

print("\n=== 所有输出文件已生成 ===")
for f in OUTPUT_DIR.glob("*.csv"):
    print(f"  - {f.name}")