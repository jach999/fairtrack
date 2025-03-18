import os

# List of files to modify
files_to_modify = [
<<<<<<< HEAD
    '/workspace/fairtrack_testing/fairtrack/ByteTrack/yolox/tracker/byte_tracker.py',
    '/workspace/fairtrack_testing/fairtrack/ByteTrack/yolox/tracker/matching.py',
=======
    '/content/fairtrack/ByteTrack/yolox/tracker/byte_tracker.py',
    '/content/fairtrack/ByteTrack/yolox/tracker/matching.py',
>>>>>>> 0c20873 (Updated project version2)
    # Add other files here if needed
]

# Function to replace 'np.bool' with 'np.bool_' and 'np.float' with 'np.float64'
def replace_np_aliases(file_path):
    with open(file_path, 'r') as file:
        file_data = file.read()

<<<<<<< HEAD
    # Only replace 'np.bool' with 'np.bool_' if 'np.bool_' is not already present
    if 'np.bool' in file_data and 'np.bool_' not in file_data:
        file_data = file_data.replace('np.bool', 'np.bool_')

    # Only replace 'np.float' with 'np.float64' if 'np.float64' is not already present
    if 'np.float' in file_data and 'np.float64' not in file_data:
        file_data = file_data.replace('np.float', 'np.float64')
=======
    # Replace deprecated aliases only if necessary
    replacements = {
        'np.bool': 'np.bool_',
        'np.float': 'np.float64'
    }
    for old, new in replacements.items():
        if old in file_data and new not in file_data:
            file_data = file_data.replace(old, new)
>>>>>>> 0c20873 (Updated project version2)

    # Write the modified data back to the file
    with open(file_path, 'w') as file:
        file.write(file_data)

    print(f"Modification completed successfully for {file_path}")

<<<<<<< HEAD
# Modify each file in the list
for file_path in files_to_modify:
    replace_np_aliases(file_path)

print("All modifications completed successfully.")
import os

# List of files to modify
files_to_modify = [
    '/workspace/fairtrack_testing/fairtrack/ByteTrack/yolox/tracker/byte_tracker.py',
    '/workspace/fairtrack_testing/fairtrack/ByteTrack/yolox/tracker/matching.py',
    # Add other files here if needed
]

# Function to replace 'np.bool' with 'np.bool_' and 'np.float' with 'np.float64'
def replace_np_aliases(file_path):
    with open(file_path, 'r') as file:
        file_data = file.read()

    # Only replace 'np.bool' with 'np.bool_' if 'np.bool_' is not already present
    if 'np.bool' in file_data and 'np.bool_' not in file_data:
        file_data = file_data.replace('np.bool', 'np.bool_')

    # Only replace 'np.float' with 'np.float64' if 'np.float64' is not already present
    if 'np.float' in file_data and 'np.float64' not in file_data:
        file_data = file_data.replace('np.float', 'np.float64')

    # Write the modified data back to the file
    with open(file_path, 'w') as file:
        file.write(file_data)

    print(f"Modification completed successfully for {file_path}")

# Modify each file in the list
for file_path in files_to_modify:
    replace_np_aliases(file_path)

print("All modifications completed successfully.")
=======
# Use a set to ensure unique file paths
unique_files = set(files_to_modify)

# Modify each unique file in the list
for file_path in unique_files:
    replace_np_aliases(file_path)

print("All modifications completed successfully.")
>>>>>>> 0c20873 (Updated project version2)
