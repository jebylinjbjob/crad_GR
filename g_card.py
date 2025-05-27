if __name__ == "__main__":
    import tkinter as tk
    from tkinter import messagebox
    import os
    from datetime import datetime, timedelta

    class CardSystemGUI:
        def __init__(self, root):
            # 基本設定
            self.root = root
            self.root.title("刷卡資料管理系統")
            self.root.geometry("1000x800")  # 放大視窗尺寸
            self.root.configure(bg='#f5f5f5')  # 設定背景色
            self.Merge_code_list = []
            self.file_path = "Merge_code.txt"
            
            # 主框架設定 
            self.main_frame = tk.Frame(self.root, padx=40, pady=40, bg='#f5f5f5')
            self.main_frame.pack(expand=True, fill='both')
            
            # 標題區塊
            title_frame = tk.Frame(self.main_frame, bg='#f5f5f5')
            title_frame.pack(pady=30)
            tk.Label(
                title_frame,
                text="刷卡資料管理系統",
                font=('微軟正黑體', 32, 'bold'),
                bg='#f5f5f5',
                fg='#2c3e50'
            ).pack()
            
            # 輸入區域
            input_frame = tk.LabelFrame(
                self.main_frame,
                text="輸入資料",
                font=('微軟正黑體', 14, 'bold'),
                padx=30,
                pady=30,
                bg='#ffffff',
                relief='groove',
                borderwidth=2
            )
            input_frame.pack(fill='x', padx=30, pady=30)
            
            # 輸入欄位樣式設定
            label_style = {'font': ('微軟正黑體', 12), 'bg': '#ffffff'}
            entry_style = {'font': ('Consolas', 12), 'width': 25}
            
            # 卡號輸入
            tk.Label(input_frame, text="卡號 (6碼):", **label_style).grid(row=0, column=0, pady=15, padx=15, sticky='e')
            self.card_code_entry = tk.Entry(input_frame, **entry_style)
            self.card_code_entry.grid(row=0, column=1, pady=15, padx=15)
            
            # 日期輸入
            tk.Label(input_frame, text="日期 (YYYYMMDD):", **label_style).grid(row=1, column=0, pady=15, padx=15, sticky='e')
            self.date_entry = tk.Entry(input_frame, **entry_style)
            self.date_entry.grid(row=1, column=1, pady=15, padx=15)
            
            # 時間輸入
            tk.Label(input_frame, text="時間 (HHMMSS):", **label_style).grid(row=2, column=0, pady=15, padx=15, sticky='e')
            self.time_entry = tk.Entry(input_frame, **entry_style)
            self.time_entry.grid(row=2, column=1, pady=15, padx=15)
            
            # 按鈕區域
            button_frame = tk.Frame(self.main_frame, bg='#f5f5f5')
            button_frame.pack(pady=30)
            
            # 按鈕樣式設定
            button_style = {
                'font': ('微軟正黑體', 12, 'bold'),
                'width': 14,
                'padx': 15,
                'pady': 8,
                'relief': 'raised',
                'borderwidth': 2,
                'cursor': 'hand2'  # 滑鼠變手指
            }
            
            # 定義不同按鈕顏色
            add_btn = tk.Button(button_frame, text="新增資料", command=self.add_record, bg='#2ecc71', fg='white', **button_style)
            show_btn = tk.Button(button_frame, text="顯示記錄", command=self.show_records, bg='#3498db', fg='white', **button_style)
            clear_btn = tk.Button(button_frame, text="清空檔案", command=self.clear_file, bg='#e74c3c', fg='white', **button_style)
            path_btn = tk.Button(button_frame, text="顯示路徑", command=self.show_path, bg='#9b59b6', fg='white', **button_style)
            auto_btn = tk.Button(button_frame, text="產生下班資料", command=self.auto_generate_data, bg='#f1c40f', fg='black', **button_style)
            
            # 按鈕排列
            for btn in [add_btn, show_btn, clear_btn, path_btn, auto_btn]:
                btn.pack(side='left', padx=12)
                
            # 顯示區域
            self.display_text = tk.Text(
                self.main_frame,
                height=14,
                width=70,
                font=('Consolas', 12),
                bg='#ffffff',
                relief='ridge',
                borderwidth=2,
                padx=10,
                pady=10
            )
            self.display_text.pack(pady=30)
            
        def auto_generate_data(self):
            time = self.time_entry.get().strip()
            card_code = self.card_code_entry.get().strip()
            date = self.date_entry.get().strip()

            self.display_text.delete(1.0, tk.END)

            # 計算時間差
            Hour = int(time[:2]) + 9
            Minute = int(time[2:4])
            Second = int(time[4:6])

            # 生成下班時間
            req_time = f"{Hour:02d}{Minute:02d}{Second:02d}"
            merge_code = f"{card_code}{date}{req_time}"

            # 驗證輸入
            if not all([
                self.validate_input(card_code, 6, "卡號"),
                self.validate_input(date, 8, "日期"), 
                self.validate_input(req_time, 6, "時間")
            ]):
                self.display_text.insert(tk.END, "請輸入正確的資料")
                return

            # 顯示格式化資訊
            display_text = f"下班時間: {req_time}\n"
            display_text += f"卡號: {card_code}\n"
            display_text += f"日期: {date}\n"
            display_text += f"刷卡資料: {merge_code}\n"

            self.display_text.insert(tk.END, display_text)
            self.Merge_code_list.append(merge_code)
            messagebox.showinfo("成功", f"已生成下班刷卡資料: {merge_code}\n請在按下新增資料輸入上班時間")

        def validate_input(self, value, length, field_name):
            if len(value) != length:
                messagebox.showerror("錯誤", f"{field_name}必須為{length}碼")
                return False
            return True

        def add_record(self):
            card_code = self.card_code_entry.get().strip()
            date = self.date_entry.get().strip()
            time = self.time_entry.get().strip()
            
            if not all([
                self.validate_input(card_code, 6, "卡號"),
                self.validate_input(date, 8, "日期"),
                self.validate_input(time, 6, "時間")
            ]):
                return
                
            merge_code = f"{card_code}{date}{time}"
            self.Merge_code_list.append(merge_code)
            
            # 更新顯示
            self.display_text.delete(1.0, tk.END)
            self.display_text.insert(tk.END, "目前輸入的刷卡資料:\n" + "="*50 + "\n")
            for idx, code in enumerate(self.Merge_code_list, 1):
                self.display_text.insert(tk.END, f"{idx}. {code}\n")
                
            # 清空輸入框
            self.card_code_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)

        def show_records(self):
            try:
                with open(self.file_path, "r") as file:
                    content = file.read()
                    self.display_text.delete(1.0, tk.END)
                    if content:
                        self.display_text.insert(tk.END, "=== 刷卡記錄 ===\n" + "="*50 + "\n")
                        self.display_text.insert(tk.END, content)
                    else:
                        self.display_text.insert(tk.END, "目前沒有任何刷卡記錄")
            except FileNotFoundError:
                messagebox.showinfo("提示", "尚未建立刷卡記錄檔案")

        def clear_file(self):
            if messagebox.askyesno("確認", "確定要清空檔案嗎?"):
                with open(self.file_path, "w") as file:
                    file.truncate(0)
                messagebox.showinfo("成功", "檔案已清空")
                self.display_text.delete(1.0, tk.END)

        def show_path(self):
            path = os.path.abspath(self.file_path)
            messagebox.showinfo("檔案路徑", f"目前TXT路徑:\n{path}")

        def save_and_exit(self):
            if self.Merge_code_list:
                with open(self.file_path, "a") as file:
                    file.write("\n".join(self.Merge_code_list) + "\n")
                messagebox.showinfo("成功", f"已儲存 {len(self.Merge_code_list)} 筆刷卡記錄")
            self.root.destroy()

    # 啟動應用程式
    root = tk.Tk()
    app = CardSystemGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.save_and_exit)
    root.mainloop()
