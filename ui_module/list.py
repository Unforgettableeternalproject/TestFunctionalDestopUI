import tkinter as tk
from sys_module.file import create_file_folder

class FunctionList:
    def __init__(self, root, on_close_callback):
        self.root = root
        self.on_close_callback = on_close_callback
        self.function_window = tk.Toplevel(root)
        self.function_window.geometry("400x600")
        self.function_window.attributes('-alpha', 0.8)  # Slight transparency
        self.function_window.overrideredirect(True)  # Remove window decorations
        self.function_window.transient(root)  # Keep it above the main window
        self.function_window.grab_set()  # Make it modal

        # Center the window
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.function_window.geometry(f"+{screen_width//2 - 200}+{screen_height//2 - 300}")

        # Exit button in the top-right corner of the function window
        exit_button = tk.Button(self.function_window, text="X", command=self.close_function_list, bg="red", fg="white")
        exit_button.place(x=370, y=10)

        # Button for creating a file/folder
        create_file_button = tk.Button(self.function_window, text="Create File/Folder", command=lambda: create_file_folder(self.function_window))
        create_file_button.pack(pady=50)

        # Force the window to appear on top
        self.function_window.lift()
        self.function_window.focus_force()

        # Variables to store the offset for dragging
        self.offset_x = 0
        self.offset_y = 0

        # Bind mouse events for dragging
        self.function_window.bind("<Button-1>", self.start_drag)
        self.function_window.bind("<B1-Motion>", self.on_drag)

    def start_drag(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def on_drag(self, event):
        x = self.function_window.winfo_x() + event.x - self.offset_x
        y = self.function_window.winfo_y() + event.y - self.offset_y
        self.function_window.geometry(f"+{x}+{y}")

    def close_function_list(self):
        self.function_window.grab_release()  # Release modal behavior
        self.function_window.destroy()  # Close the window
        self.on_close_callback()  # Re-enable the "Activate" button in the main window

# 在 main.py 中可以這樣調用
# from list import FunctionList
# function_list = FunctionList(root, on_close_callback)
