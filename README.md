### Scripts with no obscure dependencies, mac and windows friendly, interactive or with defaults, fast.  

| Script | Description |
|--------|------------|
| **videoFrameExtractor.py** | Interactive script to extract frames, super fast. OpenCV required, nothing more. Accepts file or folder input, configurable stride, and start/end frames. |
| **yobb_to_yolo_bbox.py** | Converts oriented bbox labels into normal YOLO bbox. Interactive, multithreaded, error-checking, and continues processing even on errors. If an image folder is provided, it verifies that images have their label pairs. Creates a backup before overwriting labels. |
| **mass_rename.py** | Renames label/image pairs with the same random name. Usage: `python3 script.py labels_path images_path`. |
| **resize.py** | Interactive script to resize images inside a folder using PIL. Supports interpolation methods: nearest, bilinear, bicubic, and lanczos. "All" option available for comparison. |
| **download_coco_categories.py** | Downloads specific classes from the COCO dataset, multi-threaded, and creates YOLO-format label files. Interactive with prompts and a progress bar, but also allows direct CLI usage: `py script.py 0` (class 0) or `py script.py 1,33,56,57,70 download_path`  |
| **Structure.py** | Recreates folder structure while allowing selection of how many files to copy from the original folders. Useful for creating validation datasets from training datasets. |
| **Json_to_Folders.py** | Sorts files into folders based on selected attribute values from a JSON file. Prompts for the number of files per folder with an option to process all files. |
| **videocrop_path_top_right_bot_left.py** | Crops a video by removing specified pixel amounts from its sides (top, right, bottom, left). Example usage: `py script.py video.mp4 100 0 200 20` (removes 100 pixels from top, 0 from right, 200 from bottom, 20 from left). |
| **nospaces.swift** | Removes Python-breaking characters from filenames in a chosen folder and replaces spaces with underscores. Usage: `swift nospaces.swift` (prompts for folder if not provided). Logs changes (old name → new name) in a text file within the folder. |
