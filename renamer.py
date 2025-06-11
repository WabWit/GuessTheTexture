import os
import re

def convert_potion_name(filename):
    patterns = [
        (r"(potion)__\{'minecraft__potion_contents'__\{potion__'minecraft__(.*?)'", "minecraft__{}_{}"),
        (r"(lingering_potion)__\{'minecraft__potion_contents'__\{potion__'minecraft__(.*?)'", "minecraft__{}_{}"),
        (r"(splash_potion)__\{'minecraft__potion_contents'__\{potion__'minecraft__(.*?)'", "minecraft__{}_{}"),
        (r"(tipped_arrow)__\{'minecraft__potion_contents'__\{potion__'minecraft__(.*?)'", "minecraft__{}_{}")
    ]

    for pattern, format_str in patterns:
        match = re.search(pattern, filename)
        if match:
            potion_type = match.group(1)
            effect = match.group(2)
            return format_str.format(potion_type, effect) + ".png"

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
folder_path = "./Afolder"  # Replace with your actual folder path
rename_all_potion_files(folder_path)
