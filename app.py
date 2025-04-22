import streamlit as st
import pyperclip

st.set_page_config(page_title="售價計算器 - 穿穿trytry", page_icon="🧮", layout="centered")
st.markdown("""
    <style>
        .big-font {
            font-size: 24px !important;
        }
        .suggest-box {
            background-color: #ffe6ea;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🧮 售價建議小工具")

colA, colB = st.columns(2)
with colA:
    if st.button("🔁 重新填寫所有欄位"):
        st.experimental_rerun()
with colB:
    st.button("💡 我想要功能建議！")

product_cost_rmb = st.number_input("🔻 商品成本（人民幣）", min_value=0.0, value=30.0, step=1.0, format="%.2f")
exchange_rate = st.number_input("💱 人民幣對台幣匯率", min_value=0.0, value=4.5, step=0.01, format="%.2f")
shipping_cost_per_kg = st.number_input("🚛 海運費用（台幣每公斤）", min_value=0.0, value=45.0, step=1.0, format="%.2f")
average_weight = st.number_input("⚖️ 平均重量（公斤）", min_value=0.0, value=0.5, step=0.1, format="%.2f")
fixed_cost = st.number_input("🧾 固定成本（台幣）", min_value=0.0, value=10.0, step=1.0, format="%.2f")
gross_margin = st.number_input("💰 毛利率（％）", min_value=0.0, max_value=100.0, value=60.0, step=1.0, format="%.2f")

# 計算成本與建議售價
ntd_cost = product_cost_rmb * exchange_rate + shipping_cost_per_kg * average_weight + fixed_cost
suggested_price = ntd_cost / (1 - gross_margin / 100) if gross_margin < 100 else 0
profit = suggested_price * (gross_margin / 100) if gross_margin < 100 else 0

st.markdown(f"""
<div class="suggest-box">
    <h4>🎯 建議售價：<span style='color:#d90000'>{suggested_price:.2f} 元</span></h4>
    <h5>💸 預估淨利潤：<span style='color:#008000'>{profit:.2f} 元</span></h5>
</div>
""", unsafe_allow_html=True)

# 重新填寫、複製、分享按鈕
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔁 重新填寫"):
        st.experimental_rerun()
with col2:
    if st.button("📋 複製計算結果"):
        # 將計算結果複製到剪貼簿
        result_text = f"建議售價：{suggested_price:.2f} 元\n預估淨利潤：{profit:.2f} 元"
        pyperclip.copy(result_text)
        st.success("計算結果已複製到剪貼簿！")
with col3:
    if st.button("🔗 分享此頁面"):
        st.write("分享此頁面給朋友！")
        st.markdown(f"[點此分享計算工具](https://your-deployed-streamlit-app-url)")  # 替換為你的實際分享鏈接
