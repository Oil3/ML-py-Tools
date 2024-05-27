#creates a copy of all folders but with just one random file from each.

import os
import shutil
import random

def copy_random_files(source_dir, dest_dir, num_files):
    # List all folders in the source directory
    folders = [f for f in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, f))]

    # Iterate through each folder
    for folder in folders:
        folder_path = os.path.join(source_dir, folder)
        files = os.listdir(folder_path)

        # If the folder is not empty, select a random file and copy it to the destination folder
        if files:
            selected_files = random.sample(files, min(num_files, len(files)))
            dest_folder_path = os.path.join(dest_dir, folder)
            os.makedirs(dest_folder_path, exist_ok=True)
            for selected_file in selected_files:
                source_file_path = os.path.join(folder_path, selected_file)
                shutil.copy(source_file_path, dest_folder_path)

# Prompt for the source and destination directories and number of files
source_dir = input("Enter the path of the source directory: ").strip(' "\'')
dest_dir = input("Enter the path of the destination directory: ").strip(' "\'')
num_files = int(input("Enter the number of random files to copy from each folder: "))

# Copy a random file from each folder in the source directory to the destination directory
copy_random_files(source_dir, dest_dir, num_files)

