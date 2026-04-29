from PIL import Image
import numpy as np
import os
import glob
import argparse

def load_and_scale(image_path, max_value):
    img = Image.open(image_path).convert('L')
    arr = np.array(img, dtype=np.float16)
    arr /= 255.0
    arr *= max_value
    return arr

def main():
    parser = argparse.ArgumentParser(description="Load images and scale pixel values.")
    parser.add_argument(
        "--max_val",
        type=float,
        default=2.0,
        help="Maximum value to scale the image pixel values to (default: 2.0)"
    )
    
    args = parser.parse_args()
    max_val = args.max_val
    folder = "./"

    for path in glob.glob(os.path.join(folder, "*.jpeg")):
        arr = load_and_scale(path, max_val)
        fname = os.path.basename(path)
        outname = fname[:-5]  # remove ".jpeg"
        np.save(outname, arr)

if __name__ == "__main__":
    main()
