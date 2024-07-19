**download_coco_categories.py** - downloads specific classes from the coco dataset, multi-threaded, also creates yolo-format label files for each image (detection.
![image](https://github.com/user-attachments/assets/33877648-ee9f-423f-9fa8-2103ba61dc1a)
Interactive as in prompts you what and where with then a progress bar, multi-threaded as in as fast as possible, also runnable for exemple, like `py script.py 0` for class 0 in a newfolder in current directoy, or like `py script.py 1,33,56,57,70 download_path` with specific directory. 

**Structure.py** - recreates folder structure while choosing how many files are copied from the original folders.
I use to create validation datesets from training datasets.

**Json_to_Folders.py** - sorts files into folders based on selected attributes values of a JSON file.
It prompts for the number of files to process in each folder, with the option to process all files.

**videocrop_path_top_right_bot_left.py** - Crops a video file  by removing specified amounts of pixels from its sides (top, right, bottom, left).
`py script.py video.mp4 100 0 200 20` would create a video_cropped.mp4 with 100 pixels removed from the top, 0 pixels removed from the right side, 200 pixels removed from the bottom, and 20 pixels removed from the left side.
