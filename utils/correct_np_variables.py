import os

# List of files to modify
files_to_modify = [
    '/content/fairtrack/ByteTrack/yolox/tracker/byte_tracker.py',
    '/content/fairtrack/ByteTrack/yolox/tracker/matching.py',
    # Add other files here if needed
]

# Function to replace 'np.bool' with 'np.bool_' and 'np.float' with 'np.float64'
def replace_np_aliases(file_path):
    with open(file_path, 'r') as file:
        file_data = file.read()

    # Replace deprecated aliases only if necessary
    replacements = {
        'np.bool': 'np.bool_',
        'np.float': 'np.float64'
    }
    for old, new in replacements.items():
        if old in file_data and new not in file_data:
            file_data = file_data.replace(old, new)

    # Write the modified data back to the file
    with open(file_path, 'w') as file:
        file.write(file_data)

    print(f"Modification completed successfully for {file_path}")

# Use a set to ensure unique file paths
unique_files = set(files_to_modify)

# Modify each unique file in the list
for file_path in unique_files:
    replace_np_aliases(file_path)

print("All modifications completed successfully.")