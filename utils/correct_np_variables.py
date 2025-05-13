import os

# Get the absolute path of the 'utils' directory (where this script is running)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Navigate back to the 'fairtrack' directory (parent of 'utils')
FAIRTRACK_DIR = os.path.dirname(SCRIPT_DIR)

# Construct the correct path to the target file inside 'ByteTrack/yolox/tracker'
byte_tracker_path = os.path.join(FAIRTRACK_DIR, "ByteTrack", "yolox", "tracker", "byte_tracker.py")

# Check if the file exists before proceeding
if not os.path.exists(byte_tracker_path):
    print(f"Error: File not found at {byte_tracker_path}")
else:
    print("File path resolved successfully!")

# List of files to modify (using os.path.join for cross-platform compatibility)
files_to_modify = [
    os.path.join(FAIRTRACK_DIR, "ByteTrack", "yolox", "tracker", "byte_tracker.py"),
    os.path.join(FAIRTRACK_DIR, "ByteTrack", "yolox", "tracker", "matching.py"),
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