import streamlit as st

st.set_page_config(page_title="商品售價計算機 💰", page_icon="🧮")
st.title("🧮 商品售價計算機")
st.markdown("用來計算從大陸進貨的商品售價，快速又方便 ✨")

# 預設值設定
cost_rmb = st.number_input("🐼 商品成本（人民幣）", min_value=0.0, value=00.0)
rmb_to_twd = st.number_input("💱 人民幣對台幣匯率", min_value=0.0, value=4.5)
shipping_cost = st.number_input("🚢 海運費用（台幣每公斤）", min_value=0.0, value=45.0)
weight = st.number_input("👕 每件衣服的平均重量（公斤）", min_value=0.0, value=0.5)
fixed_cost = st.number_input("🔧 固定成本（台幣）", min_value=0.0, value=0.0)
profit_margin = st.number_input("📈 毛利率（%）", min_value=0.0, max_value=100.0, value=60.0)

if st.button("📊 計算售價"):
    try:
        cost_twd = cost_rmb * rmb_to_twd
        shipping_fee = shipping_cost * weight
        total_cost = cost_twd + shipping_fee + fixed_cost
        selling_price = total_cost / (1 - profit_margin / 100)

        st.success(f"💵 建議售價（台幣）：NT$ {selling_price:.2f}")
        st.code(f"{selling_price:.2f}", language="text")

    except Exception as e:
        st.error("⚠️ 請確認輸入是否正確")
