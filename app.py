import streamlit as st
import requests
from bs4 import BeautifulSoup

# 取得人民幣即期賣出匯率
@st.cache_data(ttl=3600)
def get_rmb_rate():
    url = "https://rate.bot.com.tw/xrt?Lang=zh-TW"
    res = requests.get(url)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")
    rows = soup.select("table.table tbody tr")
    for row in rows:
        currency = row.select_one("div.hidden-phone.print_show").text.strip()
        if "人民幣" in currency:
            rate = float(row.select("td")[4].text.strip().replace(",", ""))
            return rate
    return 4.5  # fallback 值

# 預設值
defaults = {
    "cost_rmb": 0.0,
    "shipping_cost": 45.0,
    "weight": 0.5,
    "fixed_cost": 0.0,
    "profit_margin_input": 60.0,
    "roas": 5.0
}

# 設定頁面
st.set_page_config(page_title="商品售價計算機｜TryTry 工具箱", layout="centered")
st.title("🧮 商品售價計算機｜TryTry 工具箱")

# 從台灣銀行獲取最新匯率
default_rmb_rate = get_rmb_rate()

# 儲存設定的默認值
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# 輸入欄位
cost_rmb = st.number_input("🔻 商品成本（人民幣）：", min_value=0.0, format="%.2f", key="cost_rmb")
rmb_to_twd = st.number_input("💱 人民幣對台幣匯率（自動帶入，可修改）", value=default_rmb_rate, step=0.001, format="%.3f", key="rmb_to_twd")
shipping_cost = st.number_input("🚚 海運費用（台幣每公斤）：", min_value=0.0, format="%.2f", key="shipping_cost")
weight = st.number_input("⚖️ 平均重量（公斤）：", min_value=0.0, format="%.2f", key="weight")
fixed_cost = st.number_input("🧾 固定成本（台幣）：", min_value=10.0, format="%.2f", key="fixed_cost")
profit_margin_input = st.number_input("💰 期望毛利率（%）：", min_value=0.0, max_value=100.0, format="%.2f", key="profit_margin_input")
roas = st.number_input("📈 廣告 ROAS 預估值", min_value=0.0, format="%.2f", key="roas")
actual_price = st.number_input("🛒 實際售價（可選）：", min_value=0.0, format="%.2f", key="actual_price")

# 毛利率
profit_margin = profit_margin_input / 100

# 計算邏輯
def calculate_all(cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin, roas):
    cost_twd = cost_rmb * rmb_to_twd
    shipping_fee = shipping_cost * weight
    total_cost = cost_twd + shipping_fee + fixed_cost
    selling_price = total_cost / (1 - profit_margin) if profit_margin < 1 else 0
    ad_cost = selling_price / roas if roas > 0 else 0
    net_profit = selling_price - total_cost - ad_cost
    return total_cost, selling_price, ad_cost, net_profit

# 主計算
if all([cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost >= 0, profit_margin >= 0, roas >= 0]):
    total_cost, selling_price, ad_cost, net_profit = calculate_all(
        cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin, roas
    )

    st.markdown(
        f"""
        <div style="background-color:rgba(255,255,255,0.05); border-left: 5px solid #0066cc; 
                    padding: 12px 16px; border-radius: 10px;">
            <p style="color:inherit;">📦 <strong>預估進貨成本：</strong>{total_cost:.2f} 元</p>
            <p style="color:inherit;">📢 <strong>廣告成本 (ROAS={roas})：</strong>{ad_cost:.2f} 元</p>
            <p style="font-size:18px; color:inherit;"><strong>🎯 建議售價：</strong>
                <span style="font-size:20px; color:inherit;">{selling_price:.2f} 元</span>
            </p>
            <p style="color:inherit;">💸 <strong>預估淨利潤：</strong>{net_profit:.2f} 元</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if actual_price > 0:
        cost_twd = cost_rmb * rmb_to_twd
        shipping_fee = shipping_cost * weight
        total_cost = cost_twd + shipping_fee + fixed_cost
        ad_cost_actual = actual_price / roas if roas > 0 else 0
        net_profit_actual = actual_price - total_cost - ad_cost_actual
        profit_margin_actual = (actual_price - total_cost) / actual_price * 100 if actual_price > 0 else 0

        st.markdown(
            f"""
            <div style="margin-top: 20px; background-color:#f7f7f7; border-left: 5px solid #0066cc;
                        padding: 12px 16px; border-radius: 10px;">
                <p style="font-size:16px;"><strong>📊 實際售價分析結果：</strong></p>
                <p>📦 成本總額：{total_cost:.2f} 元</p>
                <p>📢 廣告成本 (ROAS={roas})：{ad_cost_actual:.2f} 元</p>
                <p>💸 淨利潤：{net_profit_actual:.2f} 元</p>
                <p>📈 毛利率：約 <strong>{profit_margin_actual:.2f}%</strong></p>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.warning("請完整填寫所有欄位以顯示計算結果。")

# 頁尾資訊
st.markdown(
    """
    <hr style="margin-top:40px;">
    <div style="text-align:center; font-size:14px; color:gray;">
        本工具由 <a href="https://s.shopee.tw/1g4QU28zE9" target="_blank"><strong>穿穿質感選物商店</strong></a> 製作提供。
    </div>
    """,
    unsafe_allow_html=True
)
