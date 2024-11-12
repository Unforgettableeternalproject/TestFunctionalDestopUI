import tkinter as tk
from .list import FunctionList

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("200x100")  # 設定視窗大小
        self.root.attributes('-alpha', 0.8)  # 設定透明度 (0.0 - 完全透明, 1.0 - 不透明)
        self.root.attributes('-topmost', True)  # 視窗保持在最上層
        self.root.overrideredirect(True)  # 移除視窗裝飾 (如標題欄)
        self.root.geometry("+1715+887") # 設定視窗位置 (X: 1715, Y: 887)

        self.offset_x = 0
        self.offset_y = 0

        # 綁定滑鼠事件以實現拖動
        self.root.bind("<Button-1>", self.start_drag)  # 左鍵點擊開始拖動
        self.root.bind("<B1-Motion>", self.on_drag)    # 按住左鍵拖動

        # 創建一個框架來容納小部件，並設置背景顏色
        self.frame = tk.Frame(self.root, bg="#282828")  # 深色背景以提高可見性
        self.frame.pack(fill="both", expand=True)

        # 添加一個按鈕來測試命令執行
        self.activate = tk.Button(self.frame, text="Activate", command=self.activate_function_list, bg="#4CAF50", fg="white", relief="flat")
        self.activate.pack(pady=20)

    def activate_function_list(self):
        # Disable the "Activate" button
        self.activate.config(state=tk.DISABLED)
        # Open the function list and pass a callback to re-enable the button
        self.list = FunctionList(self.root, lambda: self.activate.config(state=tk.NORMAL))
        
    def start_drag(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def on_drag(self, event):
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")
        
        # Debug: 顯示視窗位置
        print(f"X: {x}, Y: {y}")

    def run(self):
        self.root.mainloop()