import numpy as np
import os

H, W = 192, 256

dummy = np.ones((H,W), dtype=np.float32)
conf = np.ones((H,W), dtype=np.uint8)

out_dir = "./"
for i in range(0, 169):
    dummy.tofile(f"{out_dir}/depth_{i}.bin")
    conf.tofile(f"{out_dir}/depthConfidence_{i}.bin")
