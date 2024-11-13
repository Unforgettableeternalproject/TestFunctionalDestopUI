import tkinter as tk
from .list import FunctionList

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("200x100") 
        self.root.attributes('-alpha', 0.8) 
        self.root.attributes('-topmost', True) 
        self.root.overrideredirect(True) 
        self.root.geometry("+1715+887")

        self.offset_x = 0
        self.offset_y = 0

        self.root.bind("<Button-1>", self.start_drag) 
        self.root.bind("<B1-Motion>", self.on_drag)

        self.frame = tk.Frame(self.root, bg="#282828") 
        self.frame.pack(fill="both", expand=True)

        self.activate = tk.Button(self.frame, text="Activate", command=self.toggle_function_list, bg="#4CAF50", fg="white", relief="flat")
        self.activate.pack(pady=20)

        self.function_list = None

    def toggle_function_list(self):
        if self.function_list is None or not self.function_list.function_window.winfo_exists():
            self.activate.config(relief=tk.SUNKEN)
            self.activate.config(background="#f44336")
            self.activate.config(text="Deactivate")
            self.function_list = FunctionList(self.root, self.on_function_list_close)
            self.function_list.animate_open()
        else:
            self.function_list.animate_close()        
            self.activate.config(relief=tk.FLAT)
            self.activate.config(background="#4CAF50")
            self.activate.config(text="Activate")

    def on_function_list_close(self):
        self.function_list = None
        self.activate.config(relief=tk.FLAT)
        self.activate.config(background="#4CAF50")
        self.activate.config(text="Activate")

    def start_drag(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def on_drag(self, event):
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")

    def run(self):
        self.root.mainloop()