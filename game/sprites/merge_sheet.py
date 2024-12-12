import os
from PIL import Image

def merge_pngs(base_dir, output_file):
    # List to hold all images in the base directory
    all_images = []

    # Get a list of all PNG files in the base directory
    spritesheets = [os.path.join(base_dir, file) for file in os.listdir(base_dir) if file.endswith(".png")]
    print(f"Found {len(spritesheets)} spritesheets in {base_dir}")
    # Load all images in the base directory
    if len(spritesheets) == 0:
        print("No spritesheets found in the base directory")
        return
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
    merged_image.save(output_file)
    print(f"Merged spritesheet saved as {output_file}")

# Example usage
base_dir = "../assets/images/momo_mama"
output_file = "../assets/images/momo_mama/momo_mama.png"
merge_pngs(base_dir, output_file)