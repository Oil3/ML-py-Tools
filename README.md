**Structure.py** - recreates folder structure while choosing how many files are copied from the original folders.
I use to create validation datesets from training datasets.

**Json_to_Folders.py** - sorts files into folders based on selected attributes values of a JSON file.
It prompts for the number of files to process in each folder, with the option to process all files.

**videocrop_path_top_right_bot_left.py** - Crops a video file  by removing specified amounts of pixels from its sides (top, right, bottom, left).
`py script.py video.mp4 100 0 200 20` would create a video_cropped.mp4 with 100 pixels removed from the top, 0 pixels removed from the right side, 200 pixels removed from the bottom, and 20 pixels removed from the left side.
