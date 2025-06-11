import os

def convert_potion_name(filename):
    if not filename.endswith(".png"):
        raise ValueError("File must be a .png")

    base_name = filename[:-4]  # Remove .png

    if "__{'minecraft__potion_contents'__{potion__'minecraft__" not in base_name:
        raise ValueError("Filename structure not recognized")

    parts = base_name.split("__{'minecraft__potion_contents'__{potion__'minecraft__")
    if len(parts) != 2:
        raise ValueError("Unexpected structure in filename")

    item_type = parts[0]  # e.g., minecraft__splash_potion
    effect = parts[1].rstrip("'}")  # Remove trailing "'}"

    return f"{item_type}_{effect}.png"

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
