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
from dataclasses import dataclass
from typing import Set

import typer
from typing_extensions import Annotated

# Initialize Typer app
app = typer.Typer()

# Define the master file name
FULL_CODE_FILE_NAME: str = "full_code.txt"

FILES_TO_INCLUDE: Set[str] = set()  # if empty, include all files

# Define programming-related file extensions (removed '.json' and '.md')
PROGRAMMING_EXTENSIONS: Set[str] = {
    ".py",
    ".java",
    ".c",
    ".cpp",
    ".js",
    ".ts",
    ".html",
    ".css",
    ".rb",
    ".go",
    ".php",
    ".swift",
    ".kt",
    ".rs",
    ".scala",
    ".sh",
    ".pl",
    ".lua",
    ".sql",
    ".xml",
    ".yml",
    ".yaml",
    ".json",
}

# Define directories to exclude during file aggregation and directory tree generation
EXCLUDE_DIRS: Set[str] = {
    "venv",
    ".venv",
    "node_modules",
    "__pycache__",
    ".git",
    "dist",
    "build",
}

# Define files to exclude from both aggregation and directory tree
EXCLUDE_FILES: Set[str] = {"package-lock.json", "package.json"}


@dataclass
class Config:
    full_code_file_name: str
    files_to_include: Set[str]
    programming_extensions: Set[str]
    exclude_dirs: Set[str]


def generate_directory_tree(startpath: str, config: Config) -> str:
    """
    Generates an ASCII directory tree.
    - Excluded directories and their subdirectories are only listed by name without their internal files.
    - The script itself is excluded from the tree.

    Args:
        startpath (str): The root directory to start generating the tree from.
        config (Config): Configuration object containing settings.

    Returns:
        str: The generated directory tree as a string.
    """
    tree = ""
    for root, dirs, files in os.walk(startpath):
        # Determine the relative path from the startpath
        rel_path = os.path.relpath(root, startpath)
        if rel_path == ".":
            rel_path = ""

        # Split the relative path into parts
        path_parts = rel_path.split(os.sep) if rel_path else []

        # Calculate the level of depth
        level = len(path_parts)
        indent = "│   " * level + "├── " if level > 0 else ""

        # Add the current directory to the tree
        current_dir = (
            os.path.basename(root)
            if rel_path
            else os.path.basename(startpath.rstrip(os.sep)) or startpath
        )

        # Check if the current directory is excluded
        if current_dir in config.exclude_dirs:
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


def is_programming_file(filename: str, config: Config) -> bool:
    """
    Checks if the file has a programming-related extension.

    Args:
        filename (str): The name of the file.
        config (Config): Configuration object containing settings.

    Returns:
        bool: True if the file is a programming file, False otherwise.
    """
    _, ext = os.path.splitext(filename)
    return ext.lower() in config.programming_extensions


def should_exclude(path: str, config: Config) -> bool:
    """
    Determines if a file should be excluded based on its path.
    - Excludes files in EXCLUDE_DIRS and their subdirectories.
    - Excludes files listed in EXCLUDE_FILES.

    Args:
        path (str): The file path.
        config (Config): Configuration object containing settings.

    Returns:
        bool: True if the file should be excluded, False otherwise.
    """
    # Normalize path separators
    normalized_path = os.path.normpath(path)
    parts = normalized_path.split(os.sep)

    # Check if any part of the path is in the EXCLUDE_DIRS
    for part in parts[:-1]:  # Exclude the file name itself
        if part in config.exclude_dirs:
            return True

    # Check if the file itself is in EXCLUDE_FILES
    if parts[-1] in EXCLUDE_FILES:
        return True

    return False


def should_include_file(file_path: str, config: Config) -> bool:
    """
    Determines if a file should be included based on FILES_TO_INCLUDE.
    If FILES_TO_INCLUDE is empty, include all files.

    Args:
        file_path (str): The path to the file.
        config (Config): Configuration object containing settings.

    Returns:
        bool: True if the file should be included, False otherwise.
    """
    if not config.files_to_include:
        return True  # Include all files if the list is empty
    rel_file_path = os.path.relpath(file_path)
    return rel_file_path in config.files_to_include


@app.command()
def generate_full_code(
    full_code_file_name: Annotated[
        str,
        typer.Option(
            "--output-file",
            "-o",
            help="Name of the master file to create.",
            show_default=True,
        ),
    ] = FULL_CODE_FILE_NAME,
    files_to_include: Annotated[
        str,
        typer.Option(
            "--include-files",
            "-i",
            help="Comma-separated list of specific files to include. If not provided, all files are included.",
        ),
    ] = None,
    programming_extensions: Annotated[
        str,
        typer.Option(
            "--extensions",
            "-x",
            help=f"Comma-separated list of programming file extensions to include. Default '{', '.join(PROGRAMMING_EXTENSIONS)}'.",
            show_default=False,
        ),
    ] = None,
    exclude_dirs: Annotated[
        str,
        typer.Option(
            "--exclude-dirs",
            "-e",
            help=f"Comma-separated list of directories to join the default exclude dirs list '{', '.join(EXCLUDE_DIRS)}'",
            show_default=False,
        ),
    ] = None,
):
    """
    Generate a master file containing the directory tree and contents of specified programming files.
    """
    # Process comma-separated input strings into sets
    if files_to_include:
        files_to_include_set = set(map(str.strip, files_to_include.split(",")))
    else:
        files_to_include_set = FILES_TO_INCLUDE

    if programming_extensions:
        programming_extensions_set = set(
            map(str.strip, programming_extensions.split(","))
        )
    else:
        programming_extensions_set = PROGRAMMING_EXTENSIONS

    if exclude_dirs:
        exclude_dirs_set = EXCLUDE_DIRS.union(
            set(map(str.strip, exclude_dirs.split(",")))
        )
    else:
        exclude_dirs_set = EXCLUDE_DIRS

    # Create a Config instance
    config = Config(
        full_code_file_name=full_code_file_name,
        files_to_include=files_to_include_set,
        programming_extensions=programming_extensions_set,
        exclude_dirs=exclude_dirs_set,
    )

    startpath = os.getcwd()

    # Generate directory tree
    directory_tree = generate_directory_tree(startpath, config)

    # Open the master file for writing
    try:
        with open(config.full_code_file_name, "w", encoding="utf-8") as master_file:
            # Write the directory tree at the top
            master_file.write("Directory Tree:\n")
            master_file.write(directory_tree)
            master_file.write("\n\n")

            # Traverse the directory again to process files
            for root, dirs, files in os.walk(startpath):
                # Determine the relative path from the startpath
                rel_path = os.path.relpath(root, startpath)
                if rel_path == ".":
                    rel_path = ""

                # Split the relative path into parts
                path_parts = rel_path.split(os.sep) if rel_path else []

                # Check if any parent directory is excluded
                if any(part in config.exclude_dirs for part in path_parts):
                    # Skip processing this directory and its subdirectories
                    dirs[:] = []  # Prevent os.walk from traversing further
                    continue

                # Check if the current directory is excluded
                current_dir: str = (
                    os.path.basename(root)
                    if rel_path
                    else os.path.basename(startpath.rstrip(os.sep)) or startpath
                )
                if current_dir in config.exclude_dirs:
                    dirs[:] = []  # Prevent os.walk from traversing further
                    continue

                for file in files:
                    if not is_programming_file(file, config):
                        continue  # Skip non-programming files

                    file_path = os.path.join(root, file)
                    # Get relative path for exclusion and headers
                    rel_file_path = os.path.relpath(file_path, startpath)

                    if should_exclude(rel_file_path, config) or not should_include_file(
                        file_path, config
                    ):
                        continue  # Skip excluded files or those not in FILES_TO_INCLUDE

                    header: str = (
                        f"\n\n# ======================\n# File: {rel_file_path}\n# ======================\n\n"
                    )
                    master_file.write(header)

                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            master_file.write(content)
                    except Exception as e:
                        error_msg: str = (
                            f"\n# Error reading file {rel_file_path}: {e}\n"
                        )
                        master_file.write(error_msg)

        typer.echo(
            typer.style(
                f"Full code file '{config.full_code_file_name}' has been created successfully.",
                fg=typer.colors.GREEN,
            )
        )

    except Exception as e:
        typer.echo(
            typer.style(
                f"An error occurred while creating the full code file: {e}",
                fg=typer.colors.RED,
            )
        )
