# <class_id> <x1> <y1> <x2> <y2> <x3> <y3> <x4> <y4>
# class, x1, y1, x2, y2, x3, y3, x4, y4: image normalized coordinates of the four corners of the oriented bounding box 
#
# <class_id> <center_x> <center_y> <width> <height>
# Backup: label files are backed up to a backup/ folder before any changes are made.
# if image folder is given, checks for missing labels




import os
import shutil
import concurrent.futures
from tqdm import tqdm
import traceback

# Interactive input for the dataset directories
label_folder = input("Label folder (.txt label files): ").strip()
image_folder = input("Optional image folder (to check for missing labels,  Enter to skip): ").strip()

backup_folder = os.path.join(label_folder, "backup")
error_folder = os.path.join(label_folder, "errors") if image_folder else None

# 
if not os.path.exists(backup_folder):
    os.makedirs(backup_folder)
if error_folder and not os.path.exists(error_folder):
    os.makedirs(error_folder)

def make_backup(label_file):
    backup_path = os.path.join(backup_folder, os.path.basename(label_file))
    if not os.path.exists(backup_path):
        shutil.copy(label_file, backup_path)

def convert_oriented_bbox_to_yolo(label_file):
    """Converts coordinates-oriented bounding box annotations to YOLO format."""
    try:
        with open(label_file, 'r') as f:
            lines = f.readlines()

        # Create a backup
        make_backup(label_file)

        # Convert the oriented bounding boxes to YOLO format
        new_lines = []
        for line in lines:
            parts = line.strip().split()

            if len(parts) != 9:
                raise ValueError(f"Label format mismatch in {label_file}: expected 9 elements, got {len(parts)}")

            # Extract the class_id and coordinates of the four corners
            class_id = parts[0]
            x1, y1, x2, y2, x3, y3, x4, y4 = map(float, parts[1:])

            # Math to get the center of the bounding box
            center_x = (x1 + x2 + x3 + x4) / 4.0
            center_y = (y1 + y2 + y3 + y4) / 4.0

            # Math to get the width and height of the bounding box (axis-aligned)
            width = max(x1, x2, x3, x4) - min(x1, x2, x3, x4)
            height = max(y1, y2, y3, y4) - min(y1, y2, y3, y4)

            # Construct the new YOLO bounding box line
            new_line = f"{class_id} {center_x} {center_y} {width} {height}\n"
            new_lines.append(new_line)

            # overwrites -backup was made
        with open(label_file, 'w') as f:
            f.writelines(new_lines)

    except Exception as e:
        # If an error occurs, move the file to the error folder
        print(f"Bug processing {label_file}: {str(e)}")
        if error_folder:
            shutil.move(label_file, os.path.join(error_folder, os.path.basename(label_file)))
        return False
    return True

def process_file_pair(label_file):
    """Process each label file, check for paired image if the image folder is provided."""
    try:
        # Get the corresponding image file if an image folder is provided
        image_file = None
        if image_folder:
            image_filename = os.path.splitext(os.path.basename(label_file))[0] + ".jpg"
            image_file = os.path.join(image_folder, image_filename)

            if not os.path.exists(image_file):
                raise FileNotFoundError(f"Image file not found: {image_file}")

        # Convert the oriented bounding box to YOLO format
        success = convert_oriented_bbox_to_yolo(label_file)

        if success and image_file:
            return (label_file, image_file)  

    except Exception as e:
        print(f"Bug processing pair {label_file}: {str(e)}")
        if error_folder:
            shutil.move(label_file, os.path.join(error_folder, os.path.basename(label_file)))
            if image_file and os.path.exists(image_file):
                shutil.move(image_file, os.path.join(error_folder, os.path.basename(image_file)))
        return None

def main():
    # Gather label files from the label folder
    label_files = [os.path.join(label_folder, f) for f in os.listdir(label_folder) if f.endswith('.txt')]

    # Progress bar for tracking processing
    with tqdm(total=len(label_files), desc="Processing Labels") as pbar:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Process files concurrently
            futures = [executor.submit(process_file_pair, label_file) for label_file in label_files]

            for future in concurrent.futures.as_completed(futures):
                # Update progress bar for each completed file
                try:
                    result = future.result()
                    if result:
                        # Log successful processing
                        label_file, image_file = result
                        print(f"Successfully processed {label_file}")
                except Exception as e:
                    print(f"Bug: {traceback.format_exc()}")
                finally:
                    pbar.update(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Bug {str(e)}")
        print("Exiting...")
