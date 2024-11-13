import platform
from tkinter import simpledialog
import os
import fnmatch
from tqdm import tqdm

def create_file_folder(parent):    
    # Prompt the user to choose file or folder
    choice_dialog = simpledialog.askstring("Create", "Enter 'file' to create a .txt file or 'folder' to create a folder:", parent=parent)

    if choice_dialog and choice_dialog.lower() == "file":
        file_name_dialog = simpledialog.askstring("File Name", "Enter the name for the .txt file:", parent=parent)
        if file_name_dialog:
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

def search_files(parent):
    filename = simpledialog.askstring("Search Files", "Enter the base name or pattern of the file to search for:", parent=parent)
    if not filename: return None
    
    search_path = simpledialog.askstring("Search Path", "Enter the root directory to start searching from (default is root '/'): ", parent=parent) or "/"
    output_file = simpledialog.askstring("Output File", "Enter the name of the output file to save search results (default is 'search_results.txt'):", parent=parent) or "search_results.txt"

    if not filename:
        print("Filename is required.")
        return

    print(f"Searching for '{filename}' in '{search_path}'...")
    results = []

    # Count total directories for progress bar
    total_dirs = sum([len(dirs) for r, dirs, files in os.walk(search_path)])

    # Traverse through all directories in the specified search path
    for root, dirs, files in tqdm(os.walk(search_path), total=total_dirs, desc="Searching"):
        # Check each file in the current directory
        for name in files:
            # Check if file matches the filename pattern
            if fnmatch.fnmatch(name, f"*{filename}*"):
                # Add the full file path to results
                results.append(os.path.join(root, name))

    # Write results to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        if results:
            f.write("Search Results:\n")
            for i, file_path in enumerate(results):
                f.write(f"Result {i}: {file_path}\n")
            print(f"\n{len(results)} result(s) found. See '{output_file}' for details.")
        else:
            f.write("No files found matching the criteria.\n")
            print("\nNo results found.")

    # Open the output file for viewing
    print("Opening search results...")        
    if platform.system() == "Darwin":  # macOS
        os.system(f"open {output_file}")
    elif platform.system() == "Windows":  # Windows
        os.system(f"start {output_file}")
    elif platform.system() == "Linux":  # Linux
        os.system(f"xdg-open {output_file}")
    else:
        print("Unsupported operating system.")