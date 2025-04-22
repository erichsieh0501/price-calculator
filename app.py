import streamlit as st

st.set_page_config(page_title="成本計算器", layout="centered")

st.title("🧮 成本利潤計算器")

st.markdown("請輸入以下數值 👇")

# 成本輸入
cost_price = st.number_input("商品進價", min_value=0.0, value=100.0, step=1.0)
shipping_fee = st.number_input("運費", min_value=0.0, value=30.0, step=1.0)
advertising_cost = st.number_input("廣告費用", min_value=0.0, value=20.0, step=1.0)
extra_fee_percent = st.number_input("刷卡手續費 (%)", min_value=0.0, value=4.5, step=0.1)

# 售價輸入
selling_price = st.number_input("售價", min_value=0.0, value=250.0, step=1.0)

# 計算
total_cost = cost_price + shipping_fee + advertising_cost + (selling_price * extra_fee_percent / 100)
profit = selling_price - total_cost

st.markdown("---")
st.subheader("📊 結果")
st.write(f"🧾 總成本：NT${total_cost:.2f}")
st.write(f"💰 利潤：NT${profit:.2f}")

if profit < 0:
    st.error("🚨 你目前是虧損的唷！")
elif profit < 50:
    st.warning("⚠️ 利潤偏低，建議調整售價或成本")
else:
    st.success("✅ 有賺錢～不錯不錯！")
