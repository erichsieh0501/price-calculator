import streamlit as st

st.set_page_config(page_title="商品售價計算機｜毛利計算機", page_icon="🧮", layout="centered")
st.title("🧮 商品售價計算機｜毛利計算機")

# 👉 預設值
defaults = {
    "cost_rmb": 0.0,
    "rmb_to_twd": 4.5,
    "shipping_cost": 45.0,
    "weight": 0.5,
    "fixed_cost": 10.0,
    "profit_margin_input": 60.0
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# 👉 輸入欄位
cost_rmb = st.number_input("🔻 商品成本（人民幣）：", min_value=0.0, format="%.2f", key="cost_rmb")
rmb_to_twd = st.number_input("💱 人民幣對台幣匯率：", min_value=0.0, format="%.2f", key="rmb_to_twd")
shipping_cost = st.number_input("🚚 海運費用（台幣/公斤）：", min_value=0.0, format="%.2f", key="shipping_cost")
weight = st.number_input("⚖️ 平均重量（公斤）：", min_value=0.0, format="%.2f", key="weight")
fixed_cost = st.number_input("🧾 固定成本（台幣）：", min_value=0.0, format="%.2f", key="fixed_cost")
profit_margin_input = st.number_input("💰 毛利率（%）：", min_value=0.0, max_value=100.0, format="%.2f", key="profit_margin_input")
profit_margin = profit_margin_input / 100

# 👉 計算函式
def calculate(cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin):
    cost_twd = cost_rmb * rmb_to_twd
    shipping_fee = shipping_cost * weight
    total_cost = cost_twd + shipping_fee + fixed_cost
    suggested_price = total_cost / (1 - profit_margin) if profit_margin < 1 else 0
    profit = suggested_price * profit_margin
    return total_cost, suggested_price, profit

# 👉 顯示結果
if all([cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost]) and profit_margin < 1:
    total_cost, suggested_price, profit = calculate(
        cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin
    )

    # 預估成本
    st.markdown(
        f"""
        <div style="
            background-color: #fff8e1;
            border-left: 6px solid #ffa000;
            padding: 10px 14px;
            border-radius: 10px;
            margin-top: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <span style="font-size: 18px; font-weight: 600; color: #ff8f00;">💰 預估成本：</span>
            <span style="font-size: 24px; font-weight: bold; color: #000000;">{total_cost:.2f} 元</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 建議售價
    st.markdown(
        f"""
        <div style="
            background-color: #fff0f5;
            border-left: 6px solid #ff4b72;
            padding: 10px 14px;
            border-radius: 10px;
            margin-top: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <span style="font-size: 18px; font-weight: 600; color: #d8004c;">🎯 建議售價：</span>
            <span style="font-size: 26px; font-weight: bold; color: #000000;">{suggested_price:.2f} 元</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 預估淨利潤
    st.markdown(
        f"""
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
            <span style="font-size: 24px; font-weight: bold; color: #000000;">{profit:.2f} 元</span>
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    st.warning("請填寫所有必要欄位（成本、匯率、運費、重量、固定成本），並確認毛利率低於100%。")

# 👉 感謝訊息
st.markdown("感謝使用 穿穿質感選物商店 的售價計算工具，祝你計算愉快！")
