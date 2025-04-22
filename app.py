import streamlit as st
import streamlit.components.v1 as components

# 計算函式
def calculate_price(cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin):
    # 計算總成本
    cost_twd = cost_rmb * rmb_to_twd  # 轉換成本為台幣
    shipping_fee = shipping_cost * weight  # 計算運費
    total_cost = cost_twd + shipping_fee + fixed_cost  # 總成本
    
    # 計算售價
    selling_price = total_cost / (1 - profit_margin)  # 根據毛利率計算售價
    return selling_price

# Streamlit 應用
st.title("🧮 商品售價計算機｜毛利計算機")

# 使用者輸入欄位
cost_rmb = st.number_input("🔻 商品成本（人民幣）：", min_value=0.0, format="%.2f", value=0.0)
rmb_to_twd = st.number_input("💱 人民幣對台幣匯率：", min_value=0.0, format="%.2f", value=4.5)
shipping_cost = st.number_input("🚚 海運費用（台幣每公斤）：", min_value=0.0, format="%.2f", value=45.0)
weight = st.number_input("⚖️ 每件商品的平均重量（公斤）：", min_value=0.0, format="%.2f", value=0.5)
fixed_cost = st.number_input("🧾 固定成本（台幣）：", min_value=0.0, format="%.2f", value=10.0)
profit_margin = st.number_input("💰 毛利率（%）：", min_value=0.0, max_value=100.0, format="%.2f", value=60.0) / 100

# 計算並顯示結果
if cost_rmb and rmb_to_twd and shipping_cost and weight and fixed_cost and profit_margin:
    selling_price = calculate_price(cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin)
    
    # 顯示結果（美化版）
    components.html(
        f"""
        <div style="
            padding: 20px;
            margin-top: 30px;
            background-color: #fff0f5;
            border-left: 8px solid #ff4b72;
            border-radius: 12px;
            text-align: center;
            font-family: Arial, sans-serif;
        ">
            <h2 style="color: #d8004c; font-size: 36px; margin-bottom: 10px;">🎯 建議售價</h2>
            <p style="font-size: 40px; color: #000000; font-weight: bold;">
                {selling_price:.2f} 元
            </p>
        </div>
        """,
        height=180,
    )
else:
    st.warning("請填寫所有欄位以計算建議售價。")
