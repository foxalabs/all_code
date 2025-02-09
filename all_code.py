# Copyright 2024 Spencer Bentley

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”),
# to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import os
import argparse
import sys
import tkinter as tk
import tkinter.messagebox as messagebox
import subprocess

# Define the master file name
FULL_CODE_FILE_NAME = "full_code.txt"

FILES_TO_INCLUDE = {}  # if empty, include all files

# FILES_TO_INCLUDE = {
#     'some_file.py',
#     'another_file.js',
# }

# Define programming-related file extensions (removed '.json' and '.md')
PROGRAMMING_EXTENSIONS = {
    # General Programming Languages
    '.py', '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.vb', '.r', 
    '.rb', '.go', '.php', '.swift', '.kt', '.rs', '.scala', '.pl', '.lua',
    
    # Web Development
    '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.scss', '.less', '.sass',

    # Shell & Automation
    '.sh', '.zsh', '.fish', '.ps1', '.bat', '.cmd',

    # Database & Query Languages
    '.sql', '.psql', '.db', '.sqlite',

    # Markup & Config Files
    '.xml', '.json', '.toml', '.ini', '.yml', '.yaml', '.md', '.rst',

    # Build & Make Systems
    '.Makefile', '.gradle', '.cmake', '.ninja',

    # Other
    '.pqm', '.pq'
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
        current_dir = os.path.basename(root) if rel_path else os.path.basename(
            startpath.rstrip(os.sep)) or startpath

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


def parse_arguments():
    """
    Parses command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Aggregate code files into a master file with a directory tree.")
    parser.add_argument('-c', '--clipboard', action='store_true',
                        help="Copy the aggregated content to the clipboard instead of writing to a file.")
    parser.add_argument('-d', '--directory', type=str, default=os.getcwd(),
                        help="Specify the directory to start aggregation from. Defaults to the current working directory.")
    return parser.parse_args()

# TODO: Works on Macos. Needs Windows and Linux support
def copy_to_clipboard(content):
    try:
        process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, 
                                   stdin=subprocess.PIPE)
        process.communicate(content.encode('utf-8'))
        return True
    except Exception as e:
        print(f"Error copying to clipboard: {e}")
        return False

def main():
    args = parse_arguments()

    startpath = args.directory

    if not os.path.isdir(startpath):
        print(f"Error: The specified directory '{
              startpath}' does not exist or is not a directory.")
        sys.exit(1)

    # Generate directory tree
    directory_tree = generate_directory_tree(startpath)

    aggregated_content = "Directory Tree:\n" + directory_tree + "\n\n"

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
        current_dir = os.path.basename(root) if rel_path else os.path.basename(
            startpath.rstrip(os.sep)) or startpath
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

            header = f"\n\n# ======================\n# File: {
                rel_file_path}\n# ======================\n\n"
            aggregated_content += header

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    aggregated_content += content
            except Exception as e:
                error_msg = f"\n# Error reading file {rel_file_path}: {e}\n"
                aggregated_content += error_msg
                
    if args.clipboard:
        # Copy the aggregated content to the clipboard
        success = copy_to_clipboard(aggregated_content)
        if success:
            print("Aggregated content has been copied to the clipboard successfully.")
        else:
            print("Failed to copy aggregated content to the clipboard.")
            sys.exit(1)
    else:
        # Write the aggregated content to the master file
        try:
            with open(FULL_CODE_FILE_NAME, 'w', encoding='utf-8') as master_file:
                master_file.write(aggregated_content)
            print(f"Full code file '{
                  FULL_CODE_FILE_NAME}' has been created successfully.")
        except Exception as e:
            print(f"Error writing to file '{FULL_CODE_FILE_NAME}': {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
