from PIL import Image

# Open the background and overlay images
fid = 55
background = Image.open(f'frame_{fid}.jpg')
overlay = Image.open(f'virtual_scene_{fid}.png')

# Get the size of both images
overlay_width, overlay_height = overlay.size
background_width, background_height = background.size

# Calculate the scaling factor to preserve aspect ratio
scale = min(background_width / overlay_width, background_height / overlay_height)

# Compute the new dimensions for the overlay
new_h = int(overlay_height * scale)
new_w = int(overlay_width * scale)

# Resize the overlay image to fit the background while preserving aspect ratio
overlay_resized = overlay.resize((new_w, new_h), resample=Image.Resampling.LANCZOS)

# Make sure both images have an alpha channel (RGBA mode)
background = background.convert("RGBA")
overlay_resized = overlay_resized.convert("RGBA")

# Paste the overlay onto the background, using the alpha channel as a mask
background.paste(overlay_resized, ((background_width-new_w)//2, (background_height-new_h)//2), overlay_resized)

# Show the resulting image
background.show()
