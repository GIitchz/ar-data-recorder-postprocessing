from PIL import Image, ImageOps
import glob
import os

input_folder = "./"
output_folder = "./"

os.makedirs(output_folder, exist_ok=True)

target_w, target_h = 480, 640 

resized = 0
png = 0

for path in glob.glob(os.path.join(input_folder, "frame_*")):
    img = Image.open(path)

    w, h = img.size

    scale = min(target_w/w, target_h/h)
    img = img.resize((int(w*scale), int(h*scale)), Image.Resampling.LANCZOS)

    # STEP 2: create blank canvas (black padding)
    filename = os.path.basename(path)
    if filename[-3:]=="png":
        canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        png += 1
    else:
        canvas = Image.new("RGB", (target_w, target_h), (0, 0, 0))

    # STEP 3: center paste
    x = (target_w - img.width) // 2
    y = (target_h - img.height) // 2

    if img.mode=='RGBA':
        canvas.paste(img, (x, y), img)
    else:
        canvas.paste(img, (x, y))

    # save
    canvas.save(os.path.join(output_folder, filename))
    resized += 1

print(f"Done. Resized {resized} {png} pngs")
