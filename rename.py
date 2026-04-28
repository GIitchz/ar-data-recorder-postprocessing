import os
import re

# Folder containing your files
folder = "."

pattern = re.compile(r"virtual_(scene|depth)_(\d+)\.(png|jpeg)$", re.IGNORECASE)

for filename in os.listdir(folder):
    match = pattern.match(filename)
    if match:
        number = int(match.group(2))
        ext = match.group(3).lower()

        new_name = f"frame_{number:05d}.{ext}"

        src = os.path.join(folder, filename)
        dst = os.path.join(folder, new_name)

        print(f"Renaming: {filename} -> {new_name}")
        os.rename(src, dst)
