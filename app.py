import tkinter as tk

# 計算函式
def calculate_price():
    try:
        # 讀取使用者輸入的數值
        cost_rmb = float(cost_entry.get())  # 商品成本（人民幣）
        rmb_to_twd = float(rmb_rate_entry.get())  # 人民幣對台幣匯率
        shipping_cost = float(shipping_cost_entry.get())  # 海運費用（台幣每公斤）
        weight = float(weight_entry.get())  # 每件衣服的平均重量（公斤）
        fixed_cost = float(fixed_cost_entry.get())  # 固定成本
        profit_margin = float(profit_margin_entry.get()) / 100  # 毛利率
        
        # 計算總成本
        cost_twd = cost_rmb * rmb_to_twd  # 轉換成本為台幣
        shipping_fee = shipping_cost * weight  # 計算運費
        total_cost = cost_twd + shipping_fee + fixed_cost  # 總成本
        
        # 計算售價
        selling_price = total_cost / (1 - profit_margin)  # 根據毛利率計算售價
        
        # 顯示計算結果
        result_label.config(text=f"建議售價（台幣）：{selling_price:.2f}元 💰")
        root.update()  # 每次更新介面
        
    except ValueError:
        result_label.config(text="請確認所有輸入的數值都正確！⚠️")
        root.update()

# 創建主視窗
root = tk.Tk()
root.title("商品售價計算機 🛍️")

# 設置視窗大小
root.geometry("500x400")  # 增大視窗寬度

# 商品成本（人民幣）
tk.Label(root, text="商品成本（人民幣）：💵").grid(row=0, column=0, padx=10, pady=5, sticky='e')
cost_entry = tk.Entry(root)
cost_entry.grid(row=0, column=1, padx=20, pady=5)  # 加大右邊的間隔

# 人民幣對台幣匯率
tk.Label(root, text="人民幣對台幣匯率：💱").grid(row=1, column=0, padx=10, pady=5, sticky='e')
rmb_rate_entry = tk.Entry(root)
rmb_rate_entry.grid(row=1, column=1, padx=20, pady=5)

# 海運費用（台幣每公斤）
tk.Label(root, text="海運費用（台幣每公斤）：🚢").grid(row=2, column=0, padx=10, pady=5, sticky='e')
shipping_cost_entry = tk.Entry(root)
shipping_cost_entry.grid(row=2, column=1, padx=20, pady=5)

# 每件衣服的平均重量（公斤）
tk.Label(root, text="每件衣服的平均重量（公斤）：⚖️").grid(row=3, column=0, padx=10, pady=5, sticky='e')
weight_entry = tk.Entry(root)
weight_entry.grid(row=3, column=1, padx=20, pady=5)

# 固定成本
tk.Label(root, text="固定成本（台幣）：💸").grid(row=4, column=0, padx=10, pady=5, sticky='e')
fixed_cost_entry = tk.Entry(root)
fixed_cost_entry.grid(row=4, column=1, padx=20, pady=5)

# 毛利率
tk.Label(root, text="毛利率（%）：📈").grid(row=5, column=0, padx=10, pady=5, sticky='e')
profit_margin_entry = tk.Entry(root)
profit_margin_entry.grid(row=5, column=1, padx=20, pady=5)

# 計算按鈕
calculate_button = tk.Button(root, text="計算售價 🧮", command=calculate_price)
calculate_button.grid(row=6, column=0, columnspan=2, pady=10)

# 顯示結果
result_label = tk.Label(root, text="建議售價（台幣）：0.00元 💰")
result_label.grid(row=7, column=0, columnspan=2, pady=5)

# 開始運行應用
root.mainloop()
