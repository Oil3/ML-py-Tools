# Renames each dataset's image/label file pairs to a shortt random alphanumerical filename with a sequence number. 
# python3 script.py labels_path images_path

import os
import random
import string
import sys

def get_file_pairs(image_folder, label_folder, image_extensions=['.jpg', '.webp', '.png'], label_extension='.txt'):
    image_files = []
    label_files = []
    for root, _, files in os.walk(image_folder):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(os.path.join(root, file))
    
    for root, _, files in os.walk(label_folder):
        for file in files:
            if file.lower().endswith(label_extension):
                label_files.append(os.path.join(root, file))
    
    paired_files = []
    unpaired_images = []
    unpaired_labels = []

    for img_file in image_files:
        base_name = os.path.splitext(os.path.basename(img_file))[0]
        matching_label = None
        for lbl_file in label_files:
            if os.path.splitext(os.path.basename(lbl_file))[0] == base_name:
                matching_label = lbl_file
                break
        if matching_label:
            paired_files.append((img_file, matching_label))
        else:
            unpaired_images.append(img_file)
    
    for lbl_file in label_files:
        base_name = os.path.splitext(os.path.basename(lbl_file))[0]
        matching_image = None
        for img_file in image_files:
            if os.path.splitext(os.path.basename(img_file))[0] == base_name:
                matching_image = img_file
                break
        if not matching_image:
            unpaired_labels.append(lbl_file)

    return paired_files, unpaired_images, unpaired_labels

def generate_random_string(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def rename_files(paired_files, image_folder, label_folder):
    for i, (img_file, lbl_file) in enumerate(paired_files):
        new_base_name = f"{generate_random_string()}_{i+1:04d}"
        img_extension = os.path.splitext(img_file)[1]
        lbl_extension = os.path.splitext(lbl_file)[1]

        new_img_file = os.path.join(image_folder, new_base_name + img_extension)
        new_lbl_file = os.path.join(label_folder, new_base_name + lbl_extension)

        os.rename(img_file, new_img_file)
        os.rename(lbl_file, new_lbl_file)

        print(f"Renamed {img_file} to {new_img_file}")
        print(f"Renamed {lbl_file} to {new_lbl_file}")

def main(image_folder, label_folder):
    paired_files, unpaired_images, unpaired_labels = get_file_pairs(image_folder, label_folder)
    print(f"Found {len(paired_files)} paired files.")
    print(f"Found {len(unpaired_images)} unpaired image files.")
    print(f"Found {len(unpaired_labels)} unpaired label files.")

    if paired_files:
        rename_files(paired_files, image_folder, label_folder)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <labels_path> <images_path>")
        sys.exit(1)
    
    label_folder = sys.argv[1]
    image_folder = sys.argv[2]
    main(image_folder, label_folder)
