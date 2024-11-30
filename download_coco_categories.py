#pip install pycocotools requests tqdm
# multi-threaded interactive script to download specific class(es) from the coco dataset
# script first downloads annotations to then query user's choice(s)
# can also run like so "python3 download_coco_categories.py 0,1,2 download_path(optional, default: current directory)"
import os
import sys
import requests
from pycocotools.coco import COCO
from tqdm import tqdm
import concurrent.futures
import threading
import time

# Constants
BASE_URL = 'http://images.cocodataset.org/'
ANN_FILE = 'http://images.cocodataset.org/annotations/annotations_trainval2017.zip'
lock = threading.Lock()

def download_file(url, dest):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    os.makedirs(os.path.dirname(dest), exist_ok=True)

    with open(dest, 'wb') as file, tqdm(
        desc=dest,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]'
    ) as bar:
        start_time = time.time()
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            bar.update(len(data))
            elapsed_time = time.time() - start_time +0.01 #failsafe agains't division by 0
            bar.set_postfix(disk_used=f'{bar.n}B', total_size=f'{total_size/1024/1024:.2f}MB', download_speed=f'{(bar.n / 1024) / elapsed_time:.2f} KB/s')

def download_annotations(data_dir):
    ann_path = os.path.join(data_dir, 'annotations')
    if not os.path.exists(ann_path):
        print("Annotations not found. Downloading annotations...")
        download_file(ANN_FILE, os.path.join(data_dir, 'annotations.zip'))
        if os.name == "nt":
            os.system(f'powershell -Command "Expand-Archive -Path {os.path.join(data_dir, "annotations.zip")} -DestinationPath {data_dir}"')
        else: 
            os.system(f'unzip -q {os.path.join(data_dir, "annotations.zip")} -d {data_dir}')
       # os.remove(os.path.join(data_dir, 'annotations.zip'))
    else:
        print("Annotations already present.")

def list_categories(coco):
    categories = coco.loadCats(coco.getCatIds())
    category_names = {category['id']: category['name'] for category in categories}
    return category_names

def download_image(img, images_dir):
    img_url = BASE_URL + 'train2017/' + img['file_name']
    img_data = requests.get(img_url).content
    img_file = os.path.join(images_dir, img['file_name'])

    with open(img_file, 'wb') as handler:
        handler.write(img_data)

def create_label_file(img, anns, labels_dir, category_ids):
    label_file = os.path.join(labels_dir, f"{os.path.splitext(img['file_name'])[0]}.txt")
    with open(label_file, 'w') as lf:
        for ann in anns:
            category_id = ann['category_id']
            if category_id in category_ids:
                bbox = ann['bbox']
                x_center = (bbox[0] + bbox[2] / 2) / img['width']
                y_center = (bbox[1] + bbox[3] / 2) / img['height']
                width = bbox[2] / img['width']
                height = bbox[3] / img['height']
                lf.write(f"{category_ids.index(category_id)} {x_center} {y_center} {width} {height}\n")

def download_images_and_create_labels(data_dir, category_ids, category_names, limit=None):
    # Initialize COCO api
    coco = COCO(os.path.join(data_dir, 'annotations', 'instances_train2017.json'))

    # Get category IDs for selected categories
    imgIds = coco.getImgIds(catIds=category_ids)
    if limit:
        imgIds = imgIds[:limit]
    imgs = coco.loadImgs(imgIds)

    images_dir = os.path.join(data_dir, 'images')
    labels_dir = os.path.join(data_dir, 'labels')

    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_img = {executor.submit(download_image, img, images_dir): img for img in imgs}

        for future in tqdm(concurrent.futures.as_completed(future_to_img), total=len(imgs), desc="Downloading images and creating labels", unit="image"):
            img = future_to_img[future]
            try:
                future.result()
                # Create label file
                annIds = coco.getAnnIds(imgIds=img['id'], catIds=category_ids, iscrowd=None)
                anns = coco.loadAnns(annIds)
                create_label_file(img, anns, labels_dir, category_ids)
            except Exception as exc:
                print(f"Error downloading {img['file_name']}: {exc}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python script.py \"class_numbers(comma separated)\" \"download_path(optional, default: current directory)\"")
        class_numbers = input("Enter the category numbers you want to download, separated by commas: ")
        data_dir = input("Enter the directory to save the COCO dataset (default: coco_dataset): ").strip()
        if not data_dir:
            data_dir = 'coco_dataset'
    else:
        class_numbers = sys.argv[1]
        data_dir = sys.argv[2]

    # Download annotations
    download_annotations(data_dir)

    # Initialize COCO api to list categories
    coco = COCO(os.path.join(data_dir, 'annotations', 'instances_train2017.json'))
    category_names = list_categories(coco)

    category_indexes = [int(idx.strip()) for idx in class_numbers.split(',') if idx.strip().isdigit()]
    category_ids = list(category_names.keys())
    selected_category_ids = [category_ids[idx] for idx in category_indexes if idx < len(category_ids)]

    if not selected_category_ids:
        print("No valid categories selected. Exiting.")
        sys.exit(1)

    print(f"Downloading images and labels for categories: {', '.join([category_names[cat_id] for cat_id in selected_category_ids])}")
    # Download images for selected categories and create labels
    download_images_and_create_labels(data_dir, selected_category_ids, [category_names[cat_id] for cat_id in selected_category_ids])
