import os
import subprocess
import json
import psutil
from tkinter import simpledialog
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load constants from environment variables
APP_PATHS_FILE = os.getenv("APP_PATHS_FILE")

KNOWN_APPS = json.loads(os.getenv("KNOWN_APPS"))

CUSTOM_COMMANDS = json.loads(os.getenv("CUSTOM_COMMANDS"))

COMMON_PATHS = json.loads(os.getenv("COMMON_PATHS"))

EXECUTABLE_EXTENSIONS = json.loads(os.getenv("EXECUTABLE_EXTENSIONS"))

# Load saved application paths or create an empty dictionary
if os.path.exists(APP_PATHS_FILE):
    with open(APP_PATHS_FILE, "r") as f:
        app_paths = json.load(f)
else:
    app_paths = {}

# Function to save paths for future use
def save_app_paths():
    with open(APP_PATHS_FILE, "w") as f:
        json.dump(app_paths, f)

def is_executable(file):
    # Check if the file has an executable extension
    return any(file.lower().endswith(ext) for ext in EXECUTABLE_EXTENSIONS)

def find_application_path(app_name):
    # Check if the app path is already known
    if app_name in app_paths:
        saved_path = app_paths[app_name]
        if os.path.exists(saved_path) and is_executable(saved_path):
            return saved_path
        else:
            # Remove invalid path
            del app_paths[app_name]
            save_app_paths()
            print(f"Saved path for '{app_name}' is invalid and has been removed. Searching again...")

    # Use known app keywords to try for an exact name
    lookup_name = KNOWN_APPS.get(app_name.lower(), app_name)

    # Collect all matches
    matches = []

    # Search for the app in common directories
    for path in COMMON_PATHS:
        for root, dirs, files in os.walk(path):
            for file in files:
                if is_executable(file):
                    full_path = os.path.join(root, file)
                    # Exact match prioritization
                    if lookup_name.lower() in file.lower():
                        matches.append(full_path)
    
    # Prompt user if multiple matches are found
    if matches:
        print(f"Multiple matches found for '{app_name}':")
        for i, match in enumerate(matches, 1):
            print(f"{i}: {match}")
        try:
            choice = int(input("Enter the number of the application to open, or 0 to cancel: "))
            if choice > 0 and choice <= len(matches):
                chosen_path = matches[choice - 1]
                app_paths[app_name] = chosen_path
                save_app_paths()
                return chosen_path
        except ValueError:
            print("Invalid input. No application opened.")
    else:
        print(f"Application '{app_name}' not found.")
    
    return None

def open_application(parent):
    app_name = simpledialog.askstring("Open Application", "Enter the name of the application to try opening:", parent=parent)
    
    if not app_name: return None
    
    if app_name.lower() in CUSTOM_COMMANDS:
        custom_command = CUSTOM_COMMANDS[app_name.lower()]
        try:
            # If custom command has arguments, split for Popen
            subprocess.Popen(custom_command.split())
            print(f"Opening '{app_name}' with custom command.")
            return
        except Exception as e:
            print(f"Failed to open '{app_name}' with custom command: {e}")
            return

    # Otherwise, proceed with finding the application path by name
    path = find_application_path(app_name)
    if path:
        try:
            subprocess.Popen(path)
            print(f"Opening '{app_name}' from {path}.")
        except Exception as e:
            print(f"Failed to open '{app_name}': {e}")

def close_application(parent):
    app_name = simpledialog.askstring("Close Application", "Enter the name of the application to try closing:", parent=parent)
    
    if not app_name: return None
    
    found = False
    for proc in psutil.process_iter(['pid', 'name']):
        # Check if the app name matches the process name
        if app_name.lower() in proc.info['name'].lower():
            try:
                proc.kill()  # Terminate the process
                print(f"Successfully terminated {app_name}.")
                found = True
            except psutil.AccessDenied:
                print(f"Access denied when trying to terminate {app_name}.")
            except Exception as e:
                print(f"Failed to terminate {app_name}: {e}")
    
    if not found:
        print(f"No running instance of '{app_name}' found.")