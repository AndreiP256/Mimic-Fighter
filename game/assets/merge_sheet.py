import os
from PIL import Image

# Base directory containing the sprites
base_dir = "./images/hero"
output_dir = "./images/merged_hero"

# Make sure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# List of specific images to merge
images_to_merge = ["hero.png", "death.png"]

# List to hold all images
all_images = []

# Loop through each image and collect them
for image_name in images_to_merge:
    image_path = os.path.join(base_dir, image_name)

    # Check if the image file exists
    if not os.path.exists(image_path):
        print(f"File {image_path} does not exist.")
        continue

    # Load the image
    img = Image.open(image_path)
    all_images.append(img)

# Calculate total width and height based on individual image dimensions
total_width = max(img.width for img in all_images)  # Use the maximum width
total_height = sum(img.height for img in all_images)  # Sum of all heights

# Create a blank image with the calculated size
merged_image = Image.new("RGBA", (total_width, total_height))

# Paste each image into the new image
y_offset = 0
for img in all_images:
    merged_image.paste(img, (0, y_offset))
    y_offset += img.height

# Save the merged image
output_file = os.path.join(output_dir, "all_merged.png")
merged_image.save(output_file)
print(f"Merged spritesheet saved as {output_file}")