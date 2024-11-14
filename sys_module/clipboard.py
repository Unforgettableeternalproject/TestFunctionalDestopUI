import win32clipboard
import difflib
import threading
import time
import json
import os
import pywintypes
from tkinter import simpledialog
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# File to store clipboard history
CLIPBOARD_HISTORY_FILE = os.getenv("CLIPBOARD_HISTORY_FILE")

# Flag to control clipboard monitoring
montioring = True

# Load clipboard history from file if it exists
if os.path.exists(CLIPBOARD_HISTORY_FILE):
    with open(CLIPBOARD_HISTORY_FILE, "r") as f:
        clipboard_history = json.load(f)
else:
    clipboard_history = []
    
def save_clipboard_history():
    with open(CLIPBOARD_HISTORY_FILE, "w") as f:
        json.dump(clipboard_history, f)

def get_clipboard_text():
    for _ in range(10):  # Retry up to 10 times
        try:
            win32clipboard.OpenClipboard()
            try:
                data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
            except TypeError:
                data = None
            win32clipboard.CloseClipboard()
            return data
        except pywintypes.error as e:
            if e.args[0] == 5:  # Access denied error
                time.sleep(0.1)  # Wait for 100ms before retrying
            else:
                raise
    raise Exception("Failed to access clipboard after multiple attempts")


def monitor_clipboard():
    global monitoring
    prev_text = get_clipboard_text()
    if prev_text:
        clipboard_history.append(prev_text)
        save_clipboard_history()

    while True:
        if not montioring:
            continue
        
        current_text = get_clipboard_text()
        # Check if clipboard content has changed
        if current_text and current_text != prev_text and current_text not in clipboard_history:
            clipboard_history.append(current_text)
            save_clipboard_history()
            print(f"New clipboard entry added: {current_text}")
            prev_text = current_text
        time.sleep(1)  # Check every second

def search_clipboard(parent):
    keyword = simpledialog.askstring("Search Clipboard", "Enter a keyword to search in clipboard history:", parent=parent)
    
    if not keyword:
        return
    
    # Use difflib to find the best match in clipboard history
    matches = set(difflib.get_close_matches(keyword, clipboard_history, n=5, cutoff=0.1))
    
    if matches:
        # Print the best 5 matches for the user to choose from
        print("Best matches found:")
        for i, match in enumerate(matches, 1):
            print(f'Result {i}: "{match}"')

        # Prompt the user to choose a match
        choice = simpledialog.askinteger("Search Clipboard", "Enter the number of the result to copy to clipboard:", parent=parent)
        if choice is None or choice < 1 or choice > len(matches):
            print("Invalid choice. No clipboard history copied.")
            return None
        
        match = list(matches)[choice - 1]

        # Copy the best match back to the clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(match)
        win32clipboard.CloseClipboard()
        print(f"Copied '{match}' to clipboard.")
        return match
    else:
        print("No relevant clipboard history found.")
        return None

def remove_clipboard_history(parent):
    global clipboard_history, montioring
    confirm = simpledialog.askstring("Remove Clipboard History", "Are you sure you want to clear the clipboard history? (yes/no)", parent=parent)
    if confirm and confirm.lower() == 'yes':
        monitoring = False
        clipboard_history = []
        save_clipboard_history()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()
        print("Clipboard history cleared.")
        monitoring = True

# Start clipboard monitoring in a separate thread
monitor_thread = threading.Thread(target=monitor_clipboard, daemon=True)
monitor_thread.start()
