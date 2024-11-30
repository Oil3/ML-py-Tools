#move a percentage of images and their corresponding annotations
import os
import shutil
import random
import argparse
from pathlib import Path

def move_files(file_list, source_folder, destination_folder):
    """Move selected files from source folder to destination folder."""
    os.makedirs(destination_folder, exist_ok=True)
    for file_name in file_list:
        source_file = os.path.join(source_folder, file_name)
        destination_file = os.path.join(destination_folder, file_name)
        shutil.move(source_file, destination_file)

def select_and_move_files(images_folder, labels_folder, val_images_folder, val_labels_folder, val_percentage):
    """Select 5% of files and move them to validation folders."""
    images = [f for f in os.listdir(images_folder) if f.endswith(('.jpg', '.png', '.jpeg', '.webp'))]
    
    num_val_images = max(1, int(len(images) * val_percentage))
    val_images = random.sample(images, num_val_images)
    
    # Move images
    move_files(val_images, images_folder, val_images_folder)
    
    # Move corresponding labels
    val_labels = [Path(f).stem + '.txt' for f in val_images]
    move_files(val_labels, labels_folder, val_labels_folder)

    print(f"Moved {num_val_images} images and their corresponding labels to the validation folders.")

def main():
    parser = argparse.ArgumentParser(description="Randomly select 5% of images and labels and move them to /val/images and /val/labels folders.")
    parser.add_argument("images_folder", help="Path to the images folder.")
    parser.add_argument("labels_folder", help="Path to the labels folder.")
    parser.add_argument("val_images_folder", help="Path to the validation images folder.")
    parser.add_argument("val_labels_folder", help="Path to the validation labels folder.")
    parser.add_argument("--val_percentage", type=float, default=0.05, help="Percentage of data to move to validation. Default is 5%.")
    
    args = parser.parse_args()

    select_and_move_files(args.images_folder, args.labels_folder, args.val_images_folder, args.val_labels_folder, args.val_percentage)

if __name__ == "__main__":
    main()
