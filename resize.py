import os
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from PIL import Image

def resize_image(image_path, output_folder, width, height, resample, resample_name):
    """Resizes images of a folder, save into a new folder, Lanczos is the best quality upsampling and downsampling, also known as antialiasing."""
    try:
        with Image.open(image_path) as img:
            # Determine height if not provided to maintain aspect ratio
            if height is None:
                aspect_ratio = img.height / img.width
                height = int(width * aspect_ratio)

            # Resize the image while preserving the alpha channel if present
            resized_image = img.resize((width, height), resample=resample)

            base_name, ext = os.path.splitext(os.path.basename(image_path))
            output_path = os.path.join(output_folder, f"{base_name}_{resample_name}{ext}")
            if ext.lower() in [".jpg", ".jpeg"]:
                resized_image.save(output_path, format=img.format, quality=96) # Explicit quality because PIL's default is 75 
            elif ext.lower() == ".png":
                resized_image.save(output_path, format=img.format, compress_level=1)  # No compression for PNG
            else:
                resized_image.save(output_path, format=img.format)
            print(f"Resized and saved: {output_path}")
    except Exception as e:
        print(f"Failed to process image {image_path}: {e}")

def process_images(input_folder, output_folder, width, height, resample_methods):
    """Process all images in the input folder concurrently."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = []
        for resample_name, resample_method in resample_methods.items():
            for image_file in image_files:
                futures.append(
                    executor.submit(
                        resize_image, os.path.join(input_folder, image_file), output_folder, width, height, resample_method, resample_name
                    )
                )
        for future in as_completed(futures):
            try:
                future.result()  # To catch exceptions if any
            except Exception as exc:
                print(f"Generated an exception: {exc}")

if __name__ == "__main__":
    # Get input interactively and handle trailing whitespace
    input_folder = input("Input folder? ").strip()
    width_input = input("Width? ").strip()
    height_input = input("Height? (Default will infer height to maintain aspect ratio) ").strip()

    # Determine width and height
    width = int(width_input) if width_input else None
    height = int(height_input) if height_input else None

    if width is None:
        print("Width must be provided.")
        exit(1)

    # Ask for resampling method
    resample_map = {
        'nearest': Image.NEAREST,
        'linear': Image.BILINEAR,
        'cubic': Image.BICUBIC,
        'lanczos': Image.LANCZOS
    }
    resample_input = input("Interpolation method? (nearest/linear/cubic/lanczos/all) [default: lanczos]: ") or 'lanczos'

    if resample_input.lower() == 'all':
        resample_methods = resample_map
    else:
        resample_method = resample_map.get(resample_input.lower(), Image.LANCZOS)
        resample_methods = {resample_input.lower(): resample_method}

    # Set output folder name based on input
    output_folder = f"{input_folder}_resized"

    # Process images
    process_images(input_folder, output_folder, width, height, resample_methods)
    print(f"All images have been processed and saved in {output_folder}")
    
    """
https://www.github.com/Oil3/
    """