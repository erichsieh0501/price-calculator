import streamlit as st
import requests
from bs4 import BeautifulSoup

# 自動取得台銀人民幣匯率
@st.cache_data(ttl=3600)  # 每小時更新一次
def get_rmb_rate():
    url = "https://rate.bot.com.tw/xrt?Lang=zh-TW"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.find("table", {"title": "牌告匯率"})
    rows = table.find_all("tr")
    for row in rows:
        if "人民幣 (CNY)" in row.text:
            cells = row.find_all("td")
            # 抓「現金賣出價」
            rate = float(cells[2].text.strip())
            return rate
    return 4.5  # fallback 預設值

# 抓到匯率
default_rmb_rate = get_rmb_rate()

# 頁面設定
st.set_page_config(page_title="商品售價計算機｜TryTry 工具箱", layout="centered")
st.title("🧮 商品售價計算機｜TryTry 工具箱")

# 預設值
defaults = {
    "cost_rmb": 30.0,
    "rmb_to_twd": default_rmb_rate,
    "shipping_cost": 45.0,
    "weight": 0.5,
    "fixed_cost": 0.0,
    "profit_margin_input": 60.0,
    "roas": 5.0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# 重設按鈕
if st.button("🔁 重新填寫所有欄位"):
    for key, value in defaults.items():
        st.session_state[key] = value
    st.experimental_rerun()

# 輸入欄位
cost_rmb = st.number_input("🔻 商品成本（人民幣）", min_value=0.0, format="%.2f", key="cost_rmb")
rmb_to_twd = st.number_input("💱 人民幣對台幣匯率", min_value=0.0, format="%.2f", key="rmb_to_twd")
shipping_cost = st.number_input("🚚 海運費用（台幣每公斤）", min_value=0.0, format="%.2f", key="shipping_cost")
weight = st.number_input("⚖️ 平均重量（公斤）", min_value=0.0, format="%.2f", key="weight")
fixed_cost = st.number_input("🧾 固定成本（台幣）", min_value=0.0, format="%.2f", key="fixed_cost")
profit_margin_input = st.number_input("💰 期望毛利率（%）", min_value=0.0, max_value=100.0, format="%.2f", key="profit_margin_input")
roas = st.number_input("📈 廣告 ROAS 預估值", min_value=1.0, format="%.2f", key="roas")

profit_margin = profit_margin_input / 100

def calculate_all(cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin, roas):
    cost_twd = cost_rmb * rmb_to_twd
    shipping_fee = shipping_cost * weight
    total_cost = cost_twd + shipping_fee + fixed_cost
    if profit_margin >= 1:
        selling_price = 0
        ad_cost = 0
        net_profit = -total_cost
    else:
        selling_price = total_cost / (1 - profit_margin)
        ad_cost = selling_price / roas
        net_profit = selling_price - total_cost - ad_cost
    return total_cost, selling_price, ad_cost, net_profit

if cost_rmb > 0 and rmb_to_twd > 0 and shipping_cost >= 0 and weight >= 0 and profit_margin_input >= 0 and roas >= 1:
    total_cost, selling_price, ad_cost, net_profit = calculate_all(
        cost_rmb, rmb_to_twd, shipping_cost, weight, fixed_cost, profit_margin, roas
    )

    safe_margin = 1 - (1 - 0.18) * (1 - 1/roas) * (1 - 0.05) * (1 - 0.015)
    color = "#d8004c" if profit_margin < safe_margin else "#008000"
    status = "❗ 毛利可能不足，請再評估" if profit_margin < safe_margin else "✅ 可以賺錢喔💰"

    st.markdown(
        f"""
        <div style="background-color: #fff7f7; border-left: 6px solid {color}; padding: 12px 16px;
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
else:
    st.warning("請完整填寫所有欄位以顯示計算結果。")
