import os
import shutil
from datetime import datetime
from difflib import SequenceMatcher

# Function to organize files by chosen criteria
def organize_folder(folder_path, criteria="type"):
    # Create a dictionary to store categories based on criteria
    categories = {}

    # Iterate over each file in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            # Categorize based on the selected criteria
            if criteria == "type":
                # Group by file extension/type
                file_type = os.path.splitext(filename)[1].lower()
                if file_type not in categories:
                    categories[file_type] = []
                categories[file_type].append(filename)

            elif criteria == "time":
                # Group by file modification year and month
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                folder_name = f"{mod_time.year}_{mod_time.month:02}"
                if folder_name not in categories:
                    categories[folder_name] = []
                categories[folder_name].append(filename)

            elif criteria == "name":
                # Group by similar file names (basic implementation)
                base_name = os.path.splitext(filename)[0]
                match_found = False
                # Find similar names using SequenceMatcher
                for cat_name in categories:
                    similarity = SequenceMatcher(None, base_name, cat_name).ratio()
                    if similarity > 0.6:  # Arbitrary threshold for similarity
                        categories[cat_name].append(filename)
                        match_found = True
                        break
                if not match_found:
                    categories[base_name] = [filename]
    
    # Create folders and move files
    for category, files in categories.items():
        # Create the category folder within the target folder
        category_folder = os.path.join(folder_path, category.strip(".").replace(" ", "_"))
        os.makedirs(category_folder, exist_ok=True)

        # Move files to the category folder
        for filename in files:
            src_path = os.path.join(folder_path, filename)
            dst_path = os.path.join(category_folder, filename)
            shutil.move(src_path, dst_path)
            print(f"Moved '{filename}' to '{category_folder}'")
