import streamlit as st

st.set_page_config(page_title="商品售價計算機｜毛利計算機", page_icon="🧮", layout="centered")
st.title("🧮 商品售價計算機｜毛利計算機")

# 👉 初始化 session_state
defaults = {
    "cost_rmb": 0.0,
    "rmb_to_twd": 4.5,
    "shipping_cost": 45.0,
    "weight": 0.5,
    "fixed_cost": 10.0,
    "profit_margin_input": 60.0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# 👉 輸入欄位，讓數值更加直觀
cost_rmb = st.number_input("🔻 商品成本（人民幣）：", min_value=0.0, format="%.2f", key="cost_rmb", help="輸入商品的進貨成本")
rmb_to_twd = st.number_input("💱 人民幣對台幣匯率：", min_value=0.0, format="%.2f", key="rmb_to_twd", help="設定匯率來換算人民幣為台幣")
shipping_cost = st.number_input("🚚 海運費用（台幣每公斤）：", min_value=0.0, format="%.2f", key="shipping_cost", help="每公斤的海運費用")
weight = st.number_input("⚖️ 商品重量（公斤）：", min_value=0.0, format="%.2f", key="weight", help="商品的大概重量")
fixed_cost = st.number_input("🧾 固定成本（台幣）：", min_value=0.0, format="%.2f", key="fixed_cost", help="每個商品的固定成本，例如包裝費用")
profit_margin_input = st.number_input("💰 毛利率（%）：", min_value=0.0, max_value=100.0, format="%.2f", key="profit_margin_input", help="你想要的毛利率百分比")
profit_margin = profit_margin_input / 100

# 👉 計算售價
def calculate_price(cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin):
    cost_twd = cost_rmb * rmb_to_twd
    shipping_fee = shipping_cost * weight
    total_cost = cost_twd + shipping_fee + fixed_cost
    selling_price = total_cost / (1 - profit_margin)
    profit = selling_price * profit_margin
    return selling_price, profit

# 👉 顯示計算結果並加強視覺化
if all([cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin]):
    selling_price, profit = calculate_price(cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin)

    st.markdown(
        f"""
        <div style="
            background-color: #fff0f5;
            border-left: 6px solid #ff4b72;
            padding: 10px 14px;
            border-radius: 10px;
            margin-top: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <span style="font-size: 18px; font-weight: 600; color: #d8004c;">🎯 建議售價：</span>
            <span style="font-size: 26px; font-weight: bold; color: #000000;">{selling_price:.2f} 元</span>
        </div>
        <div style="
            background-color: #e6f7ff;
            border-left: 6px solid #00bfff;
            padding: 10px 14px;
            border-radius: 10px;
            margin-top: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <span style="font-size: 18px; font-weight: 600; color: #006bb3;">💸 預估淨利潤：</span>
            <span style="font-size: 26px; font-weight: bold; color: #000000;">{profit:.2f} 元</span>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("請填寫所有欄位以計算建議售價。")

# 👉 結束後感謝訊息（可選）
st.markdown("感謝使用 穿穿質感選物商店 的售價計算工具，祝你計算愉快！")
