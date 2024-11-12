import tkinter as tk
from .list import FunctionList

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("200x100")  # �]�w�����j�p
        self.root.attributes('-alpha', 0.8)  # �]�w�z���� (0.0 - �����z��, 1.0 - ���z��)
        self.root.attributes('-topmost', True)  # �����O���b�̤W�h
        self.root.overrideredirect(True)  # ���������˹� (�p���D��)
        self.root.geometry("+1715+887") # �]�w������m (X: 1715, Y: 887)

        self.offset_x = 0
        self.offset_y = 0

        # �j�w�ƹ��ƥ�H��{���
        self.root.bind("<Button-1>", self.start_drag)  # �����I���}�l���
        self.root.bind("<B1-Motion>", self.on_drag)    # ��������

        # �Ыؤ@�Ӯج[�Ӯe�Ǥp����A�ó]�m�I���C��
        self.frame = tk.Frame(self.root, bg="#282828")  # �`��I���H�����i����
        self.frame.pack(fill="both", expand=True)

        # �K�[�@�ӫ��s�Ӵ��թR�O����
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
        
        # Debug: ��ܵ�����m
        print(f"X: {x}, Y: {y}")

    def run(self):
        self.root.mainloop()