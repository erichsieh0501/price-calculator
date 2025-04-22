import streamlit as st

st.set_page_config(page_title="商品售價計算機｜TryTry 工具箱", layout="centered")
st.title("🧮 商品售價計算機｜TryTry 工具箱")

# 初始化預設值
defaults = {
    "cost_rmb": 0.0,
    "rmb_to_twd": 4.5,
    "shipping_cost": 45.0,
    "weight": 0.5,
    "fixed_cost": 10.0,
    "profit_margin_input": 60.0
}

# 確保 session_state 欄位存在
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# "重新填寫"按鈕
if st.button("🔁 重新填寫所有欄位"):
    for key, val in defaults.items():
        st.session_state[key] = val

# 輸入欄位
cost_rmb = st.number_input("🔻 商品成本（人民幣）：", min_value=0.0, format="%.2f", key="cost_rmb")
rmb_to_twd = st.number_input("💱 人民幣對台幣匯率：", min_value=0.0, format="%.2f", key="rmb_to_twd")
shipping_cost = st.number_input("🚚 海運費用（台幣每公斤）：", min_value=0.0, format="%.2f", key="shipping_cost")
weight = st.number_input("⚖️ 平均重量（公斤）：", min_value=0.0, format="%.2f", key="weight")
fixed_cost = st.number_input("🧾 固定成本（台幣）：", min_value=0.0, format="%.2f", key="fixed_cost")
profit_margin_input = st.number_input("💰 毛利率（%）：", min_value=0.0, max_value=100.0, format="%.2f", key="profit_margin_input")
profit_margin = profit_margin_input / 100

# 售價計算函式
def calculate_price(cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin):
    cost_twd = cost_rmb * rmb_to_twd
    shipping_fee = shipping_cost * weight
    total_cost = cost_twd + shipping_fee + fixed_cost
    return total_cost / (1 - profit_margin)

# 顯示結果和按鈕
if all([cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin]):
    selling_price = calculate_price(cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin)

    # 顯示售價卡片
    st.markdown(
        f"""
        <div style="
            background-color: #fff0f5;
            border-left: 6px solid #ff4b72;
            padding: 10px 14px;
import math

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
            margin-top: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        "">
            <span style="font-size: 18px; font-weight: 600; color: #d8004c;">🎯 建議售價：</span>
            <span style="font-size: 26px; font-weight: bold; color: #000000;">{selling_price:.2f} 元</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 一鍵複製＆分享
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("📋 複製售價", value=f"{selling_price:.2f} 元", key="copy_price")
    with col2:
        # 手動將此 URL 改為你的 Streamlit 應用地址
        app_url = "https://xzksyylptoxhc3cwjzw8kk.streamlit.app/"
        st.text_input("🔗 分享連結", value=app_url, key="share_link")
else:
    st.warning("請填寫所有欄位以計算建議售價。")
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

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔁 重新填寫"):
        st.experimental_rerun()
with col2:
    st.button("📋 複製計算結果")
with col3:
    st.button("🔗 分享此頁面")
