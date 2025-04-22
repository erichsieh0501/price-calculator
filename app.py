import streamlit as st

# 計算函式
def calculate_price(cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin):
    # 計算總成本
    cost_twd = cost_rmb * rmb_to_twd  # 轉換成本為台幣
    shipping_fee = shipping_cost * weight  # 計算運費
    total_cost = cost_twd + shipping_fee + fixed_cost  # 總成本
    
    # 計算售價
    selling_price = total_cost / (1 - profit_margin)  # 根據毛利率計算售價
    return selling_price

# 建立 Streamlit 網頁介面
st.title("商品售價計算機")

# 輸入欄位
cost_rmb = st.number_input("商品成本（人民幣）：", min_value=0.0)
rmb_to_twd = st.number_input("人民幣對台幣匯率：", min_value=4.50)
shipping_cost = st.number_input("海運費用（台幣每公斤）：", min_value=45)
weight = st.number_input("每件衣服的平均重量（公斤）：", min_value=0.5)
fixed_cost = st.number_input("固定成本（台幣）：", min_value=10)
profit_margin = st.number_input("毛利率（%）：", min_value=0.0, max_value=100.0) / 100

# 計算按鈕
if st.button("計算售價"):
    # 計算結果
    selling_price = calculate_price(cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin)
    
    # 顯示結果
    st.success(f"建議售價（台幣）：{selling_price:.2f}元")

