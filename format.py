import os
import shutil
import subprocess
import argparse

def organize_files(source_folder):
    scan_folder = os.path.join(source_folder, "scan")
    render_folder = os.path.join(source_folder, "render")
    os.makedirs(scan_folder, exist_ok=True)
    os.makedirs(render_folder, exist_ok=True)

    for file_name in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file_name)

        if file_name == "dataset.json":
            shutil.move(file_path, os.path.join(scan_folder, "capture.json"))
        elif file_name.startswith("frame_") and file_name.endswith(".jpg"):
            shutil.move(file_path, os.path.join(scan_folder, file_name))
        elif file_name.startswith("virtual_scene_") and file_name.endswith(".png"):
            shutil.move(file_path, os.path.join(render_folder, file_name))
        elif file_name.startswith("virtual_depth_") and file_name.endswith(".jpeg"):
            shutil.move(file_path, os.path.join(render_folder, file_name))

def run_post_processing_scripts(scan_folder, render_folder, max_value=None, recolor=True):
    scripts_folder = os.path.dirname(os.path.abspath(__file__))

    # Step 3: Run scripts for the 'scan' folder
    print("Running post-processing for scan folder...")
    try:
        print("flipping resolution in capture.json")
        subprocess.run(["python", os.path.join(scripts_folder, "resize_capture.py")], check=True, cwd=scan_folder)
        print("creating dummy depths")
        subprocess.run(["python", os.path.join(scripts_folder, "create_dummy_depths.py")], check=True, cwd=scan_folder)
    except subprocess.CalledProcessError as e:
        print(f"Error during post-processing in scan folder: {e}")

    # Step 4: Run scripts for the 'render' folder
    print("Running post-processing for render folder...")
    try:
        print("renaming files")
        subprocess.run(["python", os.path.join(scripts_folder, "rename.py")], check=True, cwd=render_folder)
        if recolor:
            print("recoloring depth map")
            subprocess.run(["python", os.path.join(scripts_folder,"recolor.py")], check=True, cwd=render_folder)
        print("resizing files")
        subprocess.run(["python", os.path.join(scripts_folder, "resize.py")], check=True, cwd=render_folder)
        print("creating numpy array from depthmaps")

        # Build command for convert_to_np_arr.py
        cmd = ["python", os.path.join(scripts_folder, "convert_to_np_arr.py")]
        if max_value is not None:
            print(f"taking max_val={max_value}")
            cmd += ["--max_val", str(max_value)]
        subprocess.run(cmd, check=True, cwd=render_folder)
    except subprocess.CalledProcessError as e:
        print(f"Error during post-processing in render folder: {e}")

def main():
    parser = argparse.ArgumentParser(description="Organize and process dataset files")
    parser.add_argument("source_folder", help="Path to the folder containing dataset files")
    parser.add_argument("--max_value", type=float, help="Maximum depth in the depthmap")
    parser.add_argument("--no_recolor", action="store_true", help="recolor non occupied depthmap pixels to black")

    args = parser.parse_args()
    source_folder = os.path.abspath(args.source_folder)
    max_value = args.max_value
    recolor = not args.no_recolor

    if not os.path.exists(source_folder):
        print(f"Error: Path does not exist → {source_folder}")
        return

    organize_files(source_folder)

    scan_folder = os.path.join(source_folder, "scan")
    render_folder = os.path.join(source_folder, "render")

    run_post_processing_scripts(scan_folder=scan_folder, render_folder=render_folder, max_value=max_value, recolor=recolor)

if __name__ == "__main__":
    main()
