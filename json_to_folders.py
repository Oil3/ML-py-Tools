# sorts files into folders based on selected attributes values of a JSON file. 
import os
import json

# Prompt for the location of the JSON file
json_file_path = input("Enter the path to the JSON file: ")

# Load the JSON data
with open(json_file_path, 'r') as file:
    data = json.load(file)

#This script sorts files into folders based on attributes found in a JSON file and chosen by user prompt.
#It prompts for the number of files to process in each folder, with the option to process all files.
print("Attributes found in the JSON data:")
attributes = set()
for item in data:
    for key in item.keys():
        attributes.add(key)
    for instance in item['instances']:
        for key in instance.keys():
            attributes.add(key)
print(attributes)

# Prompt for input to choose the attributes for folder names and new filenames
folder_attribute = input("Enter the attribute to use for folder names: ")
filename_attribute = input("Enter the attribute to use for new filenames: ")

# Prompt for the directory where the files are stored
file_directory = input("Enter the path to the directory where the files are stored: ")

# Prompt for the number of files to process in each folder
num_files_prompt = "Enter the number of files to process in each folder (leave blank for all): "
num_files = input(num_files_prompt)
if num_files.isdigit():
    num_files = int(num_files)
else:
    num_files = None

# Iterate through the data and move the files
for item in data:
    folder_name = item.get(folder_attribute, None)
    if folder_name is None:
        continue  # Skip this item if the folder attribute is missing
    folder_name = folder_name.strip(' "\'')

    instances = item.get('instances', [])
    # Create the directory for this folder if it doesn't exist
    folder_directory = os.path.join(file_directory, folder_name)
    if not os.path.exists(folder_directory):
        os.makedirs(folder_directory)

    # Move each file to the folder directory, up to the specified limit
    files_moved = 0
    for instance in instances:
        if num_files is not None and files_moved >= num_files:
            break  # Stop moving files if we've reached the limit

        file_name = instance.get(filename_attribute, None)
        if file_name is None:
            continue  # Skip this instance if the filename attribute is missing
        file_name = file_name.strip(' "\'')

        # Determine the file extension
        original_file_path = os.path.join(file_directory, file_name)
        _, file_extension = os.path.splitext(original_file_path)

        # Set the destination path with the correct extension
        destination_file_name = file_name + file_extension
        destination_path = os.path.join(folder_directory, destination_file_name)

        # Check if the file exists and move it
        if os.path.exists(original_file_path):
            os.rename(original_file_path, destination_path)
            print(f'Moved {destination_file_name} to {folder_directory}')
            files_moved += 1
        else:
            print(f'File {destination_file_name} not found in {file_directory}')
