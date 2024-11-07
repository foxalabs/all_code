import os

# Define the master file name
FULL_CODE_FILE_NAME = "full_code.txt"

FILES_TO_INCLUDE = {} # if empty, include all files

# FILES_TO_INCLUDE = {
#     'some_file.py',
#     'another_file.js',
# }

# Define programming-related file extensions (removed '.json' and '.md')
PROGRAMMING_EXTENSIONS = {
    '.py', '.java', '.c', '.cpp', '.js', '.ts', '.html', '.css',
    '.rb', '.go', '.php', '.swift', '.kt', '.rs', '.scala', '.sh',
    '.pl', '.lua', '.sql', '.xml', '.yml', '.yaml', 'json'
}

# Define directories to exclude during file aggregation and directory tree generation
EXCLUDE_DIRS = {
        'venv', 
        'node_modules', 
        '__pycache__', 
        '.git', 
        'dist', 
        'build',  
        'temp', 
        'old_files', 
        'flask_session'
}

# Define the name of this script to exclude it
SCRIPT_NAME = os.path.basename(__file__)

# Define files to exclude from both aggregation and directory tree
EXCLUDE_FILES = {SCRIPT_NAME, 'package-lock.json', 'package.json', 'temp.py'}

def generate_directory_tree(startpath):

#    Generates an ASCII directory tree.
#    - Excluded directories and their subdirectories are only listed by name without their internal files.
#    - The script itself is excluded from the tree.

    tree = ""
    for root, dirs, files in os.walk(startpath):
        # Determine the relative path from the startpath
        rel_path = os.path.relpath(root, startpath)
        if rel_path == '.':
            rel_path = ''

        # Split the relative path into parts
        path_parts = rel_path.split(os.sep) if rel_path else []

        # Calculate the level of depth
        level = len(path_parts)
        indent = '│   ' * level + '├── ' if level > 0 else ''

        # Add the current directory to the tree
        current_dir = os.path.basename(root) if rel_path else os.path.basename(startpath.rstrip(os.sep)) or startpath
        
        # Check if the current directory is excluded
        if current_dir in EXCLUDE_DIRS:
            tree += f"{indent}{current_dir}/ [EXCLUDED]\n"
            dirs[:] = []  # Prevent os.walk from traversing further
            continue
        
        tree += f"{indent}{current_dir}/\n"

        # List files, excluding the script itself and any in EXCLUDE_FILES
        for f in files:
            if f in EXCLUDE_FILES:
                continue  # Skip excluded files
            tree += f"{'│   ' * (level + 1)}├── {f}\n"

    return tree

def is_programming_file(filename):
    
    # Checks if the file has a programming-related extension.
    _, ext = os.path.splitext(filename)
    return ext.lower() in PROGRAMMING_EXTENSIONS

def should_exclude(path):
    # Determines if a file should be excluded based on its path.
    # - Excludes files in EXCLUDE_DIRS and their subdirectories.
    # - Excludes files listed in EXCLUDE_FILES.
    
    # Normalize path separators
    normalized_path = os.path.normpath(path)
    parts = normalized_path.split(os.sep)

    # Check if any part of the path is in the EXCLUDE_DIRS
    for part in parts[:-1]:  # Exclude the file name itself
        if part in EXCLUDE_DIRS:
            return True

    # Check if the file itself is in EXCLUDE_FILES
    if parts[-1] in EXCLUDE_FILES:
        return True

    return False

def should_include_file(file_path):
    
    # Determines if a file should be included based on FILES_TO_INCLUDE.
    # If FILES_TO_INCLUDE is empty, include all files.
    
    if not FILES_TO_INCLUDE:
        return True  # Include all files if the list is empty
    rel_file_path = os.path.relpath(file_path)
    return rel_file_path in FILES_TO_INCLUDE

def main():
    startpath = os.getcwd()

    # Generate directory tree
    directory_tree = generate_directory_tree(startpath)

    # Open the master file for writing
    with open(FULL_CODE_FILE_NAME, 'w', encoding='utf-8') as master_file:
        # Write the directory tree at the top
        master_file.write("Directory Tree:\n")
        master_file.write(directory_tree)
        master_file.write("\n\n")

        # Traverse the directory again to process files
        for root, dirs, files in os.walk(startpath):
            # Determine the relative path from the startpath
            rel_path = os.path.relpath(root, startpath)
            if rel_path == '.':
                rel_path = ''

            # Split the relative path into parts
            path_parts = rel_path.split(os.sep) if rel_path else []

            # Check if any parent directory is excluded
            if any(part in EXCLUDE_DIRS for part in path_parts):
                # Skip processing this directory and its subdirectories
                dirs[:] = []  # Prevent os.walk from traversing further
                continue

            # Check if the current directory is excluded
            current_dir = os.path.basename(root) if rel_path else os.path.basename(startpath.rstrip(os.sep)) or startpath
            if current_dir in EXCLUDE_DIRS:
                dirs[:] = []  # Prevent os.walk from traversing further
                continue

            for file in files:
                if not is_programming_file(file):
                    continue  # Skip non-programming files

                file_path = os.path.join(root, file)
                # Get relative path for exclusion and headers
                rel_file_path = os.path.relpath(file_path, startpath)

                if should_exclude(rel_file_path) or not should_include_file(file_path):
                    continue  # Skip excluded files or those not in FILES_TO_INCLUDE

                header = f"\n\n# ======================\n# File: {rel_file_path}\n# ======================\n\n"
                master_file.write(header)

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        master_file.write(content)
                except Exception as e:
                    error_msg = f"\n# Error reading file {rel_file_path}: {e}\n"
                    master_file.write(error_msg)

    print(f"Full code file '{FULL_CODE_FILE_NAME}' has been created successfully.")

if __name__ == "__main__":
    main()
