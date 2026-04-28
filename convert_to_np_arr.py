from PIL import Image
import numpy as np
import os
import glob

def load_and_scale(image_path, max_value):
    img = Image.open(image_path).convert('L')

    arr = np.array(img, dtype=np.float16)

    arr /= 255.0

    arr *= max_value

    return arr

folder = "./"
max_val = 5.0

for path in glob.glob(os.path.join(folder, "*.jpeg")):
    arr = load_and_scale(path, max_val)

    fname = os.path.basename(path)
    outname = fname[:-5]
    np.save(outname, arr)
