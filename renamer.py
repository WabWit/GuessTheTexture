import os
import re

def convert_potion_name(filename):
    patterns = [
        (r"potion__\{'minecraft__potion_contents'__\{potion__'minecraft__(.*?)'", "minecraft__potion_{}"),
        (r"lingering_potion__\{'minecraft__potion_contents'__\{potion__'minecraft__(.*?)'", "minecraft__lingering_potion_{}"),
        (r"splash_potion__\{'minecraft__potion_contents'__\{potion__'minecraft__(.*?)'", "minecraft__splash_potion_{}"),
        (r"tipped_arrow__\{'minecraft__potion_contents'__\{potion__'minecraft__(.*?)'", "minecraft__tipped_arrow_{}")
    ]

    for pattern, format_str in patterns:
        match = re.search(pattern, filename)
        if match:
            potion_type = match.group(1)
            return format_str.format(potion_type) + ".png"

    raise ValueError(f"No matching pattern for: {filename}")

def rename_all_potion_files(folder_path):
    for filename in os.listdir(folder_path):
        old_path = os.path.join(folder_path, filename)
        if os.path.isfile(old_path):
            try:
                new_filename = convert_potion_name(filename)
                new_path = os.path.join(folder_path, new_filename)

                # Remove destination file if it exists
                if os.path.exists(new_path):
                    os.remove(new_path)

                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
            except ValueError as e:
                print(f"Skipping {filename}: {e}")

# Example usage
folder_path = "./IMAGESET_VANILLA"  # Replace with your actual folder path
rename_all_potion_files(folder_path)