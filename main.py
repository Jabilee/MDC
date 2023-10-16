from PIL import Image, ImageEnhance, ImageOps
import shutil
import os
import piexif
import random
from datetime import datetime, timedelta

def clone_image(input_path, output_path):
    try:
        shutil.copy(input_path, output_path)
        print(f"Cloned {input_path} to {output_path}")
    except Exception as e:
        print(f"Error while cloning {input_path}: {str(e)}")

def add_random_null_bytes(metadata):
    # Generate a random number of null bytes (0 to 255 bytes)
    num_null_bytes = random.randint(0, 255)
    
    # Generate random null bytes
    random_null_bytes = os.urandom(num_null_bytes)
    
    # Add the random null bytes to the metadata
    metadata['0th'][piexif.ImageIFD.Software] = random_null_bytes
    
def adjust_brightness_and_saturation_and_exposure(image_path):
    try:
        image = Image.open(image_path)

        # Randomize the brightness factor (0.8 to 1.2 for minimal adjustment)
        brightness_factor = random.uniform(0.8, 1.2)

        # Randomize the saturation factor (0.8 to 1.2 for minimal adjustment)
        saturation_factor = random.uniform(0.8, 1.2)

        # Randomize the exposure factor (0.8 to 1.2 for minimal adjustment)
        exposure_factor = random.uniform(0.8, 1.2)

        # Adjust brightness
        brightness_enhancer = ImageEnhance.Brightness(image)
        image = brightness_enhancer.enhance(brightness_factor)

        # Adjust saturation
        saturation_enhancer = ImageEnhance.Color(image)
        image = saturation_enhancer.enhance(saturation_factor)

        # Adjust exposure
        exposure_enhancer = ImageEnhance.Brightness(image)
        adjusted_image = exposure_enhancer.enhance(exposure_factor)

        # Save the adjusted image
        adjusted_image.save(image_path)
        print(f"Adjusted brightness, saturation, and exposure for {image_path} with factors {brightness_factor:.2f}, {saturation_factor:.2f}, and {exposure_factor:.2f}")
    except Exception as e:
        print(f"Error while adjusting brightness, saturation, and exposure for {image_path}: {str(e)}")

def generate_random_date_time():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    random_date = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
    return random_date.strftime('%Y:%m:%d %H:%M:%S')

def modify_metadata(image_path, custom_date_time):
    try:
        exif_data = piexif.load(image_path)

        # Set custom date and time in EXIF metadata
        exif_data['Exif'][piexif.ExifIFD.DateTimeOriginal] = custom_date_time
        exif_data['Exif'][piexif.ExifIFD.DateTimeDigitized] = custom_date_time

        # Add random null bytes to metadata
        add_random_null_bytes(exif_data)

        # Save the modified metadata
        exif_bytes = piexif.dump(exif_data)
        piexif.insert(exif_bytes, image_path)

        print(f"Modified metadata for {image_path}")
    except Exception as e:
        print(f"Error while modifying metadata for {image_path}: {str(e)}")

# Define the input and output directories, the number of clones, and the number of photos to apply filters to
input_dir = "input_images"
output_dir = "output_images"
num_clones = 2  # Change this to the desired number of clones per image
num_photos_to_apply_filters = 1  # Number of photos to apply brightness, saturation, and exposure to

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate through input images
for filename in os.listdir(input_dir):
    if filename.endswith((".jpg", ".jpeg", ".png")):
        input_path = os.path.join(input_dir, filename)

        for i in range(num_clones):
            output_filename = f"{os.path.splitext(filename)[0]}_{i}{os.path.splitext(filename)[1]}"
            output_path = os.path.join(output_dir, output_filename)

            random_date_time = generate_random_date_time()
            clone_image(input_path, output_path)

            if i < num_photos_to_apply_filters:
                adjust_brightness_and_saturation_and_exposure(output_path)  # Apply all adjustments to a specified number of photos
            else:
                modify_metadata(output_path, random_date_time)  # Apply metadata modification to the rest
