import pandas as pd
import numpy as np
import random
import os

np.random.seed(42)
random.seed(42)

output_dir = r'c:\Users\32655\Documents\trae_projects\7141'

# ============================================================
# 1. 生成模拟用户数据
# ============================================================
print("=" * 60)
print("1. 生成模拟用户数据")
print("=" * 60)

n_users = 5000

customer_ids = ['CUST' + str(i).zfill(5) for i in range(1, n_users + 1)]
churn = np.random.choice(['Yes', 'No'], n_users, p=[0.15, 0.85])
tenure = np.random.randint(0, 73, n_users)
preferred_login_device = np.random.choice(['Mobile Phone', 'Phone', 'Computer'], n_users, p=[0.45, 0.25, 0.3])
city_tier = np.random.choice([1, 2, 3, 4], n_users, p=[0.3, 0.35, 0.25, 0.1])
warehouse_to_home = np.random.randint(5, 100, n_users)
preferred_payment_mode = np.random.choice(['Cash on Delivery', 'COD', 'Credit Card', 'Debit Card', 'E-wallet'], n_users, p=[0.25, 0.2, 0.2, 0.15, 0.2])
gender = np.random.choice(['Male', 'Female'], n_users, p=[0.52, 0.48])
hour_spend_on_app = np.round(np.random.uniform(0, 5, n_users), 2)
number_of_device_registered = np.random.randint(1, 6, n_users)
prefered_order_cat = np.random.choice(['Mobile', 'Laptop', 'Fashion', 'Electronics', 'Grocery'], n_users)
satisfaction_score = np.random.randint(1, 6, n_users)
marital_status = np.random.choice(['Single', 'Married', 'Divorced'], n_users, p=[0.4, 0.5, 0.1])
number_of_address = np.random.randint(1, 6, n_users)
complain = np.random.choice(['Yes', 'No'], n_users, p=[0.05, 0.95])
order_amount_hike_from_last_year = np.round(np.random.uniform(-20, 100, n_users), 1)
coupon_used = np.random.randint(0, 20, n_users)
order_count = np.random.randint(1, 50, n_users)
day_since_last_order = np.random.randint(0, 90, n_users)
cashback_amount = np.round(np.random.uniform(0, 500, n_users), 2)

df_users = pd.DataFrame({
    'CustomerID': customer_ids,
    'Churn': churn,
    'Tenure': tenure,
    'PreferredLoginDevice': preferred_login_device,
    'CityTier': city_tier,
    'WarehouseToHome': warehouse_to_home,
    'PreferredPaymentMode': preferred_payment_mode,
    'Gender': gender,
    'HourSpendOnApp': hour_spend_on_app,
    'NumberOfDeviceRegistered': number_of_device_registered,
    'PreferedOrderCat': prefered_order_cat,
    'SatisfactionScore': satisfaction_score,
    'MaritalStatus': marital_status,
    'NumberOfAddress': number_of_address,
    'Complain': complain,
    'OrderAmountHikeFromlastYear': order_amount_hike_from_last_year,
    'CouponUsed': coupon_used,
    'OrderCount': order_count,
    'DaySinceLastOrder': day_since_last_order,
    'CashbackAmount': cashback_amount
})

# 随机添加缺失值 (10%比例)
for col in df_users.columns:
    if col != 'CustomerID':
        mask = np.random.random(n_users) < 0.1
        df_users.loc[mask, col] = np.nan

print(f"生成用户数据: {df_users.shape[0]} 行, {df_users.shape[1]} 列")

# ============================================================
# 2. 输出每个字段的缺失数量和缺失比例
# ============================================================
print("\n" + "=" * 60)
print("2. 用户数据缺失统计")
print("=" * 60)

missing_stats = pd.DataFrame({
    '缺失数量': df_users.isnull().sum(),
    '缺失比例': (df_users.isnull().sum() / len(df_users) * 100).round(2)
})
print(missing_stats)

# ============================================================
# 3. 用中位数填补数值缺失值
# ============================================================
print("\n" + "=" * 60)
print("3. 用中位数填补数值缺失值")
print("=" * 60)

numeric_cols = df_users.select_dtypes(include=[np.number]).columns.tolist()
for col in numeric_cols:
    median_val = df_users[col].median()
    missing_count = df_users[col].isnull().sum()
    df_users[col] = df_users[col].fillna(median_val)
    print(f"{col}: 填补 {missing_count} 个缺失值, 中位数 = {median_val}")

# ============================================================
# 4. 统一 Phone 与 Mobile Phone
# ============================================================
print("\n" + "=" * 60)
print("4. 统一 Phone 与 Mobile Phone")
print("=" * 60)

print(f"统一前 - Mobile Phone: {(df_users['PreferredLoginDevice'] == 'Mobile Phone').sum()}")
print(f"统一前 - Phone: {(df_users['PreferredLoginDevice'] == 'Phone').sum()}")

df_users['PreferredLoginDevice'] = df_users['PreferredLoginDevice'].replace('Phone', 'Mobile Phone')

print(f"统一后 - Mobile Phone: {(df_users['PreferredLoginDevice'] == 'Mobile Phone').sum()}")

# ============================================================
# 5. 统一 COD 与 Cash on Delivery
# ============================================================
print("\n" + "=" * 60)
print("5. 统一 COD 与 Cash on Delivery")
print("=" * 60)

print(f"统一前 - Cash on Delivery: {(df_users['PreferredPaymentMode'] == 'Cash on Delivery').sum()}")
print(f"统一前 - COD: {(df_users['PreferredPaymentMode'] == 'COD').sum()}")

df_users['PreferredPaymentMode'] = df_users['PreferredPaymentMode'].replace('COD', 'Cash on Delivery')

print(f"统一后 - Cash on Delivery: {(df_users['PreferredPaymentMode'] == 'Cash on Delivery').sum()}")

# ============================================================
# 6. IQR 候选异常值检查 (WarehouseToHome, OrderCount, CashbackAmount)
# ============================================================
print("\n" + "=" * 60)
print("6. IQR 候选异常值检查")
print("=" * 60)

def iqr_outliers(df, col):
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    return outliers, lower_bound, upper_bound

check_cols = ['WarehouseToHome', 'OrderCount', 'CashbackAmount']
for col in check_cols:
    outliers, lower, upper = iqr_outliers(df_users, col)
    print(f"\n{col}:")
    print(f"  四分位距 (IQR): {df_users[col].quantile(0.75) - df_users[col].quantile(0.25):.2f}")
    print(f"  下界: {lower:.2f}, 上界: {upper:.2f}")
    print(f"  候选异常值数量: {len(outliers)}")
    print(f"  候选异常值占比: {(len(outliers)/len(df_users)*100):.2f}%")

# ============================================================
# 7. 处理淘宝数据 - 清理商品ID隐藏空白字符
# ============================================================
print("\n" + "=" * 60)
print("7. 处理淘宝数据 - 清理商品ID隐藏空白字符")
print("=" * 60)

taobao_path = os.path.join(output_dir, '淘宝全品类全国数据.csv')
df_taobao = pd.read_csv(taobao_path)

print(f"读取淘宝数据: {df_taobao.shape[0]} 行")
print(f"商品id字段前5个值(清理前):")
print(df_taobao['商品id'].head())

df_taobao['商品id'] = df_taobao['商品id'].astype(str).str.replace(r'\\t', '', regex=True).str.strip()

print(f"\n商品id字段前5个值(清理后):")
print(df_taobao['商品id'].head())

# ============================================================
# 8. 处理淘宝数据 - 先用后付和退货宝缺失值填充为"未提供"
# ============================================================
print("\n" + "=" * 60)
print("8. 处理淘宝数据 - 先用后付和退货宝缺失值填充")
print("=" * 60)

for col in ['先用后付', '退货宝']:
    missing_count = df_taobao[col].isnull().sum()
    df_taobao[col] = df_taobao[col].fillna('未提供')
    print(f"{col}: 填补 {missing_count} 个缺失值")

# ============================================================
# 9. 处理淘宝数据 - 新建"销量下限"字段
# ============================================================
print("\n" + "=" * 60)
print("9. 处理淘宝数据 - 新建销量下限字段")
print("=" * 60)

def extract_sales_lower(volume_str):
    volume_str = str(volume_str)
    if '万+' in volume_str:
        num = float(volume_str.replace('万+人付款', '').replace('万+', ''))
        return int(num * 10000)
    elif '+' in volume_str:
        return int(volume_str.replace('+人付款', '').replace('+', ''))
    else:
        try:
            return int(volume_str)
        except:
            return 0

df_taobao['销量下限'] = df_taobao['商品销量'].apply(extract_sales_lower)

print(f"销量下限字段示例:")
print(df_taobao[['商品销量', '销量下限']].head(10))

# ============================================================
# 10. 导出清洗后的CSV文件
# ============================================================
print("\n" + "=" * 60)
print("10. 导出清洗后的CSV文件")
print("=" * 60)

users_output_path = os.path.join(output_dir, '用户数据_清洗后.csv')
taobao_output_path = os.path.join(output_dir, '淘宝数据_清洗后.csv')

df_users.to_csv(users_output_path, index=False, encoding='utf-8-sig')
df_taobao.to_csv(taobao_output_path, index=False, encoding='utf-8-sig')

print(f"用户数据已导出: {users_output_path}")
print(f"淘宝数据已导出: {taobao_output_path}")

# ============================================================
# 11. 三句话总结
# ============================================================
print("\n" + "=" * 60)
print("11. 清洗总结")
print("=" * 60)
print("""
本次清洗主要完成了：用户数据的缺失值处理（中位数填充数值型、统一文本值）、异常值检查（IQR方法），以及淘宝数据的商品ID清理、缺失值填充和销量下限字段计算。

每一步的原因：中位数填充能避免均值受极端值影响，统一同义词确保数据一致性，IQR检查帮助识别潜在异常，清理空白字符防止匹配错误，销量下限字段便于后续数值分析。

需要业务确认的结论：IQR识别出的候选异常值是否为真实异常（可能是合理的极端值），先用后付和退货宝字段中"未提供"的含义是否准确反映业务场景。
""")

print("\n数据清洗完成！")