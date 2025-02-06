# interactive super-fast video frame extractor
# takes a folder or a video file as input, stride, start frame  and end frame
# default input is current folder, default stride and start/end frames are 1 to process complete video.

import cv2
import os
import sys
import datetime
import threading
import queue
from tqdm import tqdm

cv2.setUseOptimized(False)

def get_video_stats(video_path):
    """Get frame count, FPS, and duration of a video."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Cannot open video file {video_path}")
        return None, None, None

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fpss = cap.get(cv2.CAP_PROP_FPS)
    fps = round(fpss)
    duration = frame_count / fps if fps else None
    width = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return frame_count, fps, duration, width, height

def save_worker(frame_queue, output_folder, video_name, stop_event):
    """Threaded function for saving frames."""
    while not stop_event.is_set() or not frame_queue.empty():
        try:
            frame_num, frame = frame_queue.get(timeout=1)
        except queue.Empty:
            continue  # Avoid CPU overuse by waiting instead of spinning

        output_path = os.path.join(output_folder, f"{frame_num}_{video_name}.jpg")
        cv2.imwrite(output_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 96])
        frame_queue.task_done()

def extract_frames(video_path, output_folder, stride=1, start_frame=1, end_frame=None, num_workers=8):
    """Extract frames sequentially in memory and save them using multiple threads."""
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    video_output_folder = os.path.join(output_folder, video_name)
    os.makedirs(video_output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Cannot open {video_path}")
        return

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if end_frame is None or end_frame > frame_count:
        end_frame = frame_count

    frame_queue = queue.Queue(maxsize=64)  
    stop_event = threading.Event()

    # Multiple worker threads for saving frames, which coupled with in-memory frame extraction, makes it significantly faster than else-how. 
    workers = []
    for _ in range(num_workers):
        t = threading.Thread(target=save_worker, args=(frame_queue, video_output_folder, video_name, stop_event))
        t.start()
        workers.append(t)

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    total_frames = (end_frame - start_frame) // stride
    pbar = tqdm(total=total_frames, desc=f"Extracting {video_name}", unit="frame")

    frame_num = start_frame
    skipped = 0
    while frame_num < end_frame:
        ret, frame = cap.read()
        if not ret:
            skipped += 1
            frame_num += stride 
            continue  # Skip buggy frame and proceed

        frame_queue.put((frame_num, frame)) # Put frame in queue

        frame_num += stride  # Move forward by stride
        pbar.update(1)

    cap.release()
    pbar.close()

    # Wait for the queue to be empty
    frame_queue.join()
    stop_event.set()

    # Wait for threads to finish
    for t in workers:
        t.join()

    print(f"\n✅ Done processing {video_name}, skipped {skipped} unreadable frames")
    print(f"📂 Output folder: {video_output_folder}")

def get_valid_path(prompt, default):
    """Handles path and its eventual spaces, quotes, and escape characters."""
    while True:
        path = input(f"{prompt} [{default}]: ").strip() or default

        # Remove surrounding quotes if pasted with them
        if path.startswith(("'", '"')) and path.endswith(("'", '"')):
            path = path[1:-1]

        # Expand ~ to the full home directory if used
        path = os.path.expanduser(path)

        # Convert to absolute path for reliability
        path = os.path.abspath(path)

        if os.path.exists(path):
            return path
        print(f"Path error: {path}\nTry again.")

def main():
    now = datetime.datetime.now().strftime("%d%H%M")
    default_output = os.path.abspath(f"output_{now}")

    if len(sys.argv) < 2:
        # Interactive mode
        input_path = get_valid_path("Input file/folder?", os.getcwd())
        output_folder = os.path.abspath(default_output)
        os.makedirs(output_folder, exist_ok=True)

        try:
            stride = int(input("Stride? (default 1)") or 1)
            start_frame = int(input("Start frame? (default 1)") or 1)
        except ValueError:
            print("Invalid input, using defaults.")
            stride, start_frame = 1, 1

        print(f"📂 Output folder: {output_folder}")
    else:
        # Command-line arguments mode
        input_path = os.path.abspath(sys.argv[1])
        stride = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        output_folder = default_output
        os.makedirs(output_folder, exist_ok=True)

    # Process video(s)
    if os.path.isdir(input_path):
        video_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    else:
        video_files = [input_path]

    for video in video_files:
        frame_count, fps, duration, width, height = get_video_stats(video)
        if frame_count is None:
            continue

        print(f"\n🎥 Processing {video} \n🎥  {frame_count} frames, {duration:.2f}s, FPS: {fps}, Size: {width}x{height}")
        extract_frames(video, output_folder, stride=stride, start_frame=start_frame, num_workers=8)

    print(f"\n✅ Completed. Output folder: {output_folder}")

if __name__ == "__main__":
    main()
