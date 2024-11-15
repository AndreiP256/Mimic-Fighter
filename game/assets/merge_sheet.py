import os
from PIL import Image

# Base directory containing the sprites
base_dir = "./images/hero"
output_dir = "./images/merged_hero"

# Make sure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# List of directions to merge
directions = ["Up", "Right", "Down"]

# List to hold all images
all_images = []

# Loop through each direction folder and collect images
for direction in directions:
    direction_path = os.path.join(base_dir, direction)

    # Check if the direction folder exists
    if not os.path.exists(direction_path):
        print(f"Directory {direction_path} does not exist.")
        continue

    # Get a list of all PNG files in the direction folder
    spritesheets = [os.path.join(direction_path, file) for file in os.listdir(direction_path) if file.endswith(".png")]

    # Load all images in the folder
    images = [Image.open(sheet) for sheet in spritesheets]
    all_images.extend(images)

# Calculate total width and height based on individual image dimensions
total_width = max(img.width for img in all_images)  # Use the maximum width
total_height = sum(img.height for img in all_images)  # Sum of all heights

# Create a blank image with the calculated size
merged_image = Image.new("RGBA", (total_width, total_height))

# Paste each spritesheet into the new image
y_offset = 0
for img in all_images:
    merged_image.paste(img, (0, y_offset))
    y_offset += img.height

# Save the merged image
output_file = os.path.join(output_dir, "all_merged.png")
merged_image.save(output_file)
print(f"Merged spritesheet saved as {output_file}")