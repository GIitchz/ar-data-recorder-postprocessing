import json

input_file = "capture.json"
output_file = "capture.json"

with open(input_file, "r") as f:
    data = json.load(f)

# case 1: structure is {"frames": [...]}
if "frames" in data:
    for frame in data["frames"]:
        if "resolution" in frame:
            frame["resolution"] = [480, 640]

# case 2: flat list of frames
elif isinstance(data, list):
    for frame in data:
        if "resolution" in frame:
            frame["resolution"] = [480, 640]

# save result
with open(output_file, "w") as f:
    json.dump(data, f, indent=2)

print("Done. Saved to", output_file)
