import streamlit as st

# 計算函式
def calculate_price(cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin):
    cost_twd = cost_rmb * rmb_to_twd
    shipping_fee = shipping_cost * weight
    total_cost = cost_twd + shipping_fee + fixed_cost
    selling_price = total_cost / (1 - profit_margin)
    return selling_price

# Streamlit 應用
st.title("🧮 商品售價計算機｜TryTry 工具箱")

# 使用者輸入欄位
cost_rmb = st.number_input("🔻 商品成本（人民幣）：", min_value=0.0, format="%.2f", value=0.0)
rmb_to_twd = st.number_input("💱 人民幣對台幣匯率：", min_value=0.0, format="%.2f", value=4.5)
shipping_cost = st.number_input("🚚 海運費用（台幣每公斤）：", min_value=0.0, format="%.2f", value=45.0)
weight = st.number_input("⚖️ 平均重量（公斤）：", min_value=0.0, format="%.2f", value=0.5)
fixed_cost = st.number_input("🧾 固定成本（台幣）：", min_value=0.0, format="%.2f", value=10.0)
profit_margin = st.number_input("💰 毛利率（%）：", min_value=0.0, max_value=100.0, format="%.2f", value=60.0) / 100

# 顯示建議售價
if all([cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin]):
    selling_price = calculate_price(cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin)

    # 更小巧的樣式設計
    st.markdown(
        f"""
        <div style="
            background-color: #fff0f5;
            border-left: 6px solid #ff4b72;
            padding: 12px 16px;
            border-radius: 10px;
            margin-top: 18px;
        ">
            <h4 style="color: #d8004c; margin-bottom: 4px;">🎯 建議售價：</h4>
            <p style="font-size: 26px; font-weight: bold; color: #000000; margin: 0;">
                {selling_price:.2f} 元
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("請填寫所有欄位以計算建議售價。")
