from PIL import Image

# Load the spritesheet
input_file = "./images/merged_hero/test.png"  # Path to the uploaded file
output_file = "images/hero/new_image.png"  # Path to save the shifted spritesheet

# Open the spritesheet
spritesheet = Image.open(input_file)

# Get dimensions of the spritesheet
width, height = spritesheet.size

# Create a new blank image with the same dimensions as the spritesheet
shifted_spritesheet = Image.new("RGBA", (width + 10, height))  # Add extra width for shifting

# Paste the spritesheet onto the new image, shifted by 10 pixels to the right
shifted_spritesheet.paste(spritesheet, (10, 0))

# Save the modified spritesheet
shifted_spritesheet.save(output_file)

print(f"Shifted spritesheet saved at: {output_file}")
