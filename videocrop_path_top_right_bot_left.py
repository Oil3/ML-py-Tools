#Takes a video file and crops it by removing specified amounts of pixels from its sides (top, right, bottom, left)
#For exemple, to remove 100 pixels from the top of the video and 20 from bottom: python3 script.py video.mp4 100 0 20 0 
 
import cv2
import os
import sys
import subprocess

def crop_video(file_path, top, bottom, left, right):
    cap = cv2.VideoCapture(file_path)
    
    if not cap.isOpened():
        print(f"Error opening video file: {file_path}")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    new_width = frame_width - left - right
    new_height = frame_height - top - bottom

    if new_width <= 0 or new_height <= 0:
        print("Cropping dimensions are too large, resulting in non-positive frame dimensions.")
        return

    # Define the codec and create VideoWriter object
    output_path = os.path.splitext(file_path)[0] + "_cropped_temp.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'avc1')  # H264 codec
    out = cv2.VideoWriter(output_path, fourcc, fps, (new_width, new_height))

    for _ in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break

        # Crop the frame
        cropped_frame = frame[top:top+new_height, left:left+new_width]
        
        # Write the cropped frame
        out.write(cropped_frame)

    # Release everything if job is finished
    cap.release()
    out.release()
    print(f"Temporary cropped video saved as {output_path}")

    # Re-encode the video with a higher bitrate using ffmpeg
    final_output_path = os.path.splitext(file_path)[0] + "_cropped.mp4"
    ffmpeg_command = [
        'ffmpeg', '-i', output_path, '-c:v', 'libx264', '-b:v', '5M', '-c:a', 'copy', final_output_path
    ]
    subprocess.run(ffmpeg_command)

    # Remove the temporary file
    os.remove(output_path)
    print(f"Final cropped video saved as {final_output_path}")

def main():
    if len(sys.argv) != 6:
        print("Usage: python script.py <file_path> <top> <bottom> <left> <right>")
        return

    file_path = sys.argv[1]
    top = int(sys.argv[2])
    bottom = int(sys.argv[3])
    left = int(sys.argv[4])
    right = int(sys.argv[5])

    crop_video(file_path, top, bottom, left, right)

if __name__ == "__main__":
    main()
