import os
import sys
import site

# Get the correct path to 'site-packages' dynamically
site_packages_path = site.getsitepackages()[0]  # Gets the first site-packages directory
supervision_path = os.normpath(os.path.join(site_packages_path, "lib\site-packages\supervision\detection\core.py"))  # Construct full path

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