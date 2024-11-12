import tkinter as tk
from tkinter import simpledialog
import os

def create_file_folder(parent):
    # Temporarily release the grab to allow the dialog to be on top
    parent.grab_release()
    parent.lift()  # Ensure dialog is above other windows
    parent.focus_force()  # Focus on the dialog
    
    # Prompt the user to choose file or folder
    choice_dialog = simpledialog.askstring("Create", "Enter 'file' to create a .txt file or 'folder' to create a folder:", parent=parent)

    if choice_dialog and choice_dialog.lower() == "file":
        file_name_dialog = simpledialog.askstring("File Name", "Enter the name for the .txt file:", parent=parent)
        if file_name_dialog:
            file_name_dialog.lift()
            file_name_dialog.focus_force()
            with open(f"{file_name_dialog}.txt", "w") as f:
                f.write("This is a new file.")
            print(f"{file_name_dialog}.txt created.")
    elif choice_dialog and choice_dialog.lower() == "folder":
        folder_name_dialog = simpledialog.askstring("Folder Name", "Enter the name for the folder:", parent=parent)
        if folder_name_dialog:
            os.makedirs(folder_name_dialog, exist_ok=True)
            print(f"Folder '{folder_name_dialog}' created.")
    else:
        print("Invalid input. Please enter 'file' or 'folder'.")
        
    # Re-acquire the grab after the dialog is closed
    parent.grab_set()
