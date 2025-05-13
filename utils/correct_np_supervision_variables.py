import os
import site

# Correct path of 'site-packages' 
site_packages_path = site.getsitepackages()[0]

# File to modify path
supervision_path = os.path.normpath(os.path.join(site_packages_path, "supervision/detection/core.py"))

# Verify if file exists
if not os.path.exists(supervision_path):
    print(f"Error: file not found in: {supervision_path}")
else:
    print(f"File found in: {supervision_path}")

# List of files to modify (now using dynamic path detection)
files_to_modify = [supervision_path]

# Replacements to make
replacements = {
    'np.bool': 'np.bool_',
    'np.float': 'np.float64'
}

def replace_variables(file_path):
    try:
        with open(file_path, 'r') as file:
            file_data = file.read()

        for old_var, new_var in replacements.items():
            if old_var in file_data and new_var not in file_data:
                file_data = file_data.replace(old_var, new_var)
        
        with open(file_path, 'w') as file:
            file.write(file_data)

        print(f"Replacements made successfully in {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Run the replacements on detected paths
for file_path in files_to_modify:
    if os.path.exists(file_path):  # Check if file exists before modifying
        replace_variables(file_path)
    else:
        print(f"File not found: {file_path}")