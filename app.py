import streamlit as st

# 計算函式
def calculate_price(cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin):
    cost_twd = cost_rmb * rmb_to_twd
    shipping_fee = shipping_cost * weight
    total_cost = cost_twd + shipping_fee + fixed_cost
    selling_price = total_cost / (1 - profit_margin)
    return selling_price

# Streamlit 應用
st.set_page_config(page_title="商品售價計算機｜TryTry 工具箱", layout="centered")
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
        """,
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔁 重新計算"):
            st.experimental_rerun()

    with col2:
        st.code(f"{selling_price:.2f} 元", language="plaintext")
        st.button("📋 複製售價", on_click=st.toast, args=(f"已複製：{selling_price:.2f} 元",))

    with col3:
        current_url = st.secrets.get("app_url", "https://your-calc-link.streamlit.app/")
        st.code(current_url, language="plaintext")
        st.button("🔗 分享連結", on_click=st.toast, args=("連結已複製 ✅",))

else:
    st.warning("請填寫所有欄位以計算建議售價。")
