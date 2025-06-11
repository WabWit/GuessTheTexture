import os

def write_filenames_to_txt(folder_path, output_txt_path):
    with open(output_txt_path, 'w') as file:
        for filename in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, filename)):
                file.write(f'"{filename}"\n')
    print(f"File names written to {output_txt_path}")

# Example usage
folder_path = "./IMAGESET_VANILLA"  # Replace with your folder
output_txt_path = "./filenames.txt"  # Output text file
write_filenames_to_txt(folder_path, output_txt_path)