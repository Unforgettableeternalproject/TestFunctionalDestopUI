import tkinter as tk
from sys_module.file import create_file_folder, search_files
from sys_module.apps import open_application, close_application
from sys_module.clipboard import search_clipboard, remove_clipboard_history

class FunctionList:
    def __init__(self, root, on_close_callback):
        self.root = root
        self.on_close_callback = on_close_callback
        self.is_busy = False
        self.closing = False

        self.function_window = tk.Toplevel(root)
        self.function_window.geometry("400x600")
        self.function_window.attributes('-topmost', True) 
        self.function_window.attributes('-alpha', 0.9)  # Slight transparency
        self.function_window.overrideredirect(True)  # Remove window decorations
        self.function_window.transient(root)  # Keep it above the main window

        # Center the window
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.center_x = screen_width // 2
        self.center_y = screen_height // 2
        self.function_window.geometry(f"+{self.center_x - 200}+{self.center_y - 300}")

        # Create a frame for the content
        self.content_frame = tk.Frame(self.function_window, bg="#333333")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Add a title
        title_label = tk.Label(self.content_frame, text="Function List", bg="#333333", fg="white", font=("Arial", 16))
        title_label.pack(pady=10)

        # Create a panel for the functions
        self.function_panel = tk.Frame(self.content_frame, bg="#444444")
        self.function_panel.pack(fill="both", expand=True, pady=10)

        # Add sample functions
        self.add_function("Create File/Folder", create_file_folder)
        self.add_function("Search Files", search_files)
        self.add_function("Open Application", open_application)
        self.add_function("Close Application", close_application)
        self.add_function("Search Clipboard", search_clipboard)
        self.add_function("Remove Clipboard History", remove_clipboard_history)

        # Force the window to appear on top
        self.function_window.lift()
        self.function_window.focus_force()

        # Variables to store the offset for dragging
        self.offset_x = 0
        self.offset_y = 0

        # Bind mouse events for dragging
        self.function_window.bind("<Button-1>", self.start_drag)
        self.function_window.bind("<B1-Motion>", self.on_drag)

        # Bind focus out event
        self.function_window.bind("<FocusOut>", self.on_focus_out)

    def start_drag(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def on_drag(self, event):
        x = self.function_window.winfo_x() + event.x - self.offset_x
        y = self.function_window.winfo_y() + event.y - self.offset_y
        self.function_window.geometry(f"+{x}+{y}")

    def on_focus_out(self, event):
        if not self.is_busy:
            self.function_window.attributes('-topmost', True)
            self.function_window.after(100, self.animate_close())
            self.function_window.attributes('-topmost', False)

    def animate_open(self):
        self.function_window.geometry("0x0")
        self._animate(0, 0, 400, 600)

    def animate_close(self):
        try:
            self._animate(400, 600, 0, 0, self.close_function_list)
        except:
            self.close_function_list()

    def _animate(self, start_width, start_height, end_width, end_height, callback=None):
        step = 10
        width_diff = (end_width - start_width) // step
        height_diff = (end_height - start_height) // step

        def animate_step(current_step):
            if current_step <= step:
                new_width = start_width + width_diff * current_step
                new_height = start_height + height_diff * current_step
                new_x = self.center_x - new_width // 2
                new_y = self.center_y - new_height // 2
                if self.function_window.winfo_exists():
                    self.function_window.geometry(f"{new_width}x{new_height}+{new_x}+{new_y}")
                    self.root.after(10, animate_step, current_step + 1)
                else:
                    print("Window does not exist")
            else:
                if callback:
                    callback()

        animate_step(0)

    def close_function_list(self):
        if not self.closing:
            self.closing = True
            self.function_window.destroy()  # Close the window
            self.on_close_callback()  # Re-enable the "Activate" button in the main window

    def add_function(self, label_text, command):
        function_frame = tk.Frame(self.function_panel, bg="#555555", pady=5)
        function_frame.pack(fill="x", pady=5)

        label = tk.Label(function_frame, text=label_text, bg="#555555", fg="white", font=("Arial", 12))
        label.pack(side="left", padx=10)

        button = tk.Button(function_frame, text="Invoke", command=lambda: self.invoke_function(command), bg="#4CAF50", fg="white")
        button.pack(side="right", padx=10)

    def invoke_function(self, command):
        self.function_window.attributes('-topmost', False) 
        self.is_busy = True
        command(self.function_window)
        self.is_busy = False
        self.root.focus_force()
        self.function_window.attributes('-topmost', True)