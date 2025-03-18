# List of files to modify (directly specify the paths involved in your error)
files_to_modify = [
    '/usr/local/lib/python3.11/dist-packages/supervision/detection/core.py',
    # Add other file paths here if needed
]

# Replacements to make (key: old variable, value: new variable)
replacements = {
    'np.bool': 'np.bool_',
    'np.float': 'np.float64'
}

# Function to replace deprecated variables in the file
def replace_variables(file_path):
    try:
        # Open the file and read its content
        with open(file_path, 'r') as file:
            file_data = file.read()

        # Perform replacements
        for old_var, new_var in replacements.items():
            if old_var in file_data and new_var not in file_data:
                file_data = file_data.replace(old_var, new_var)
        
        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.write(file_data)

        print(f"Replacements made successfully in {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Modify each file in the list
for file_path in files_to_modify:
    replace_variables(file_path)

print("All modifications completed successfully.")
