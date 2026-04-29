from PIL import Image
import os

input_dir = "./"
output_dir = "./"

count = 0
for filename in os.listdir(input_dir):
    if filename.endswith(".png"):
        base = filename[:-4]
        png_path = os.path.join(input_dir, base + ".png")
        jpg_path = os.path.join(input_dir, base + ".jpeg")

        if not os.path.exists(jpg_path):
            continue

        count += 1

        png = Image.open(png_path).convert("RGBA")
        jpg = Image.open(jpg_path).convert("RGB")

        png_pixels = png.load()
        jpg_pixels = jpg.load()

        w, h = png.size

        for y in range(h):
            for x in range(w):
                _, _, _, a = png_pixels[x, y]
                if a == 0:
                    jpg_pixels[x, y] = (0, 0, 0)

        output_path = os.path.join(output_dir, base + ".jpeg")
        jpg.save(output_path, "JPEG")

print(f"Done. {count} files recolored")
