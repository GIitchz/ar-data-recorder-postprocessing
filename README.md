For the virtual scene data:  
rename.py - renames virtual_* files into the proper frame_%05d format  
resize.py - expects files to be renamed first. Resizes it to match the real scene's resolution (value hardcoded in code for now)  
convert_to_np_arr.py - converts the virtual scene's depth data into a numpy array. Max depth is set to 2.  

<br>

For real scene data:  
create_dummy_depths.py - creates dummy initial depth files  
resize_capture.py - flips capture.json's resolution field values to make it match the format expected.  
