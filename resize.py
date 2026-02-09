from PIL import Image
import os
import argparse

def resize_images_if_tall(folder_path, target_height=491):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if not os.path.isfile(file_path):
            continue

        try:
            with Image.open(file_path) as img:
                if img.height <= target_height:
                    print(f"Skipped (≤491px): {filename}")
                    continue

                width = int((img.width * target_height) / img.height)
                resized_img = img.resize((width, target_height), Image.Resampling.LANCZOS)
                resized_img.save(file_path, optimize=True, quality=95)
                print(f"Resized: {filename} → {width}x{target_height}")
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize images in a folder if taller than 491px.")
    parser.add_argument("folder", help="Path to the image folder")
    args = parser.parse_args()
    
    resize_images_if_tall(args.folder)   