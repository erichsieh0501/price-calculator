import streamlit as st

st.set_page_config(page_title="商品售價計算機｜TryTry 工具箱", layout="centered")

st.markdown("""
    <style>
    /* 手機優化：讓輸入欄位佔滿寬度 */
    .stNumberInput > div > div {
        width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧮 商品售價計算機｜TryTry 工具箱")

# 預設值
defaults = {
    "cost_rmb": 30.0,
    "rmb_to_twd": 4.5,
    "shipping_cost": 45.0,
    "weight": 0.5,
    "fixed_cost": 0.0,
    "profit_margin_input": 60.0,
    "roas": 5.0
}

# 初始化狀態
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# 重設按鈕
with st.expander("🔁 重新填寫"):
    if st.button("點我重設所有欄位"):
        for key, value in defaults.items():
            st.session_state[key] = value
        st.experimental_rerun()

# 表單開始
with st.form("form"):
    st.subheader("請輸入商品成本與參數")

    cost_rmb = st.number_input("🔻 商品成本（人民幣）", min_value=0.0, format="%.2f", key="cost_rmb")
    rmb_to_twd = st.number_input("💱 匯率（人民幣➡台幣）", min_value=0.0, format="%.2f", key="rmb_to_twd")
    shipping_cost = st.number_input("🚚 海運費用（台幣/公斤）", min_value=0.0, format="%.2f", key="shipping_cost")
    weight = st.number_input("⚖️ 商品重量（公斤）", min_value=0.0, format="%.2f", key="weight")
    fixed_cost = st.number_input("🧾 固定成本（台幣）", min_value=0.0, format="%.2f", key="fixed_cost")
    profit_margin_input = st.number_input("💰 想要的毛利率（%）", min_value=0.0, max_value=100.0, format="%.2f", key="profit_margin_input")
    roas = st.number_input("📈 預估 ROAS（建議填 5~6）", min_value=1.0, format="%.2f", key="roas")

    submitted = st.form_submit_button("🚀 計算建議售價")

# 計算函式
def calculate_all(cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin, roas):
    cost_twd = cost_rmb * rmb_to_twd
    shipping_fee = shipping_cost * weight
    total_cost = cost_twd + shipping_fee + fixed_cost
    selling_price = total_cost / (1 - profit_margin) if profit_margin < 1 else 0
    ad_cost = selling_price / roas
    net_profit = selling_price - total_cost - ad_cost
    return total_cost, selling_price, ad_cost, net_profit

if submitted:
    profit_margin = profit_margin_input / 100

    total_cost, selling_price, ad_cost, net_profit = calculate_all(
        cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin, roas
    )

    # 安全毛利率門檻計算（考慮平台抽成/廣告/金流）
    safe_margin = 1 - (1 - 0.18) * (1 - 1/roas) * (1 - 0.05) * (1 - 0.015)

    # 狀態色彩
    color = "#d8004c" if profit_margin < safe_margin else "#008000"
    status = "❗ 毛利可能不足，請再評估" if profit_margin < safe_margin else "✅ 可以賺錢喔💰"

    # 顯示區塊
    st.markdown(
        f"""
        <div style="background-color: #fff7f7; border-left: 6px solid {color}; padding: 14px 20px;
                    border-radius: 10px; margin-top: 20px;">
            <p style="font-size:18px;">📦 <strong>預估總成本</strong>：{total_cost:.2f} 元</p>
            <p style="font-size:18px;">📢 <strong>預估廣告成本</strong>（ROAS = {roas}）：{ad_cost:.2f} 元</p>
            <p style="font-size:20px;"><strong>🎯 建議售價</strong>：<span style="font-size:24px; color:#000000;">{selling_price:.2f} 元</span></p>
            <p style="font-size:18px;">💸 <strong>預估淨利潤</strong>：{net_profit:.2f} 元</p>
            <p style="color: {color}; font-weight: bold; font-size: 16px;">{status}</p>
        </div>
        """,
        unsafe_allow_html=True
    )