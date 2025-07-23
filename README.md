# All Code Aggregator

## Overview

The **All Code Aggregator** script consolidates all programming-related code files in the current directory into a single `full_code.txt` file. This is especially useful for providing your entire codebase to AI models for analysis or assistance.

## Features

- **Directory Tree Generation**: Creates an ASCII representation of the directory structure, excluding specified directories.
- **Code Aggregation**: Combines contents of programming-related files into a master file.
- **Customizable Inclusions/Exclusions**: Easily specify which files or directories to include or exclude.
- **Clipboard Output**: Use `-c` to copy the results directly to your clipboard on macOS and Windows 10+.

## Setup

1. **From Github**

```shell
pip install git+https://github.com/foxalabs/all_code@0.4.0
```

2. **From local directory**

To install from a local directory, use edit mode so your code changes are reflected immediately. This is useful for development/debugging mode.
```shell
git clone https://github.com/foxalabs/all_code.git
cd all_code
pip install -e .
```

## Usage
**Basic usage**
```bash
all-code
```

**Specify a Directory**
```bash
all-code -d /path/to/start/directory
```

**Copy Aggregated Content to Clipboard Instead of Writing to File** (macOS and Windows 10+)
```bash
all-code -c
```

**Combine Both Arguments: Specify Directory and Copy to Clipboard**
```bash
all-code -d /path/to/start/directory -c
```

**Exclude Specific File Extensions**
```bash
all-code -X .json,.md,.html
```
**Combine Multiple Options: Specify Directory, Copy to Clipboard, and Exclude Extensions**
```bash
all-code -d /path/to/start/directory -c -X .json,.md,.html
```

**More options**
```bash
all-code --help
usage: all_code.py [-h] [-c] [-d DIRECTORY] [-o OUTPUT_FILE] [-i INCLUDE_FILES] [-x EXTENSIONS] [-e EXCLUDE_DIRS]

Aggregate code files into a master file with a directory tree.

options:
  -h, --help            show this help message and exit
  -c, --clipboard       Copy the aggregated content to the clipboard instead of writing to a file.
  -d, --directory DIRECTORY
                        Specify the directory to start aggregation from. Defaults to the current working directory.
  -o, --output-file OUTPUT_FILE
                        Name of the output file. Defaults to full_code.txt.
  -i, --include-files INCLUDE_FILES
                        Comma-separated list of files to include. If not provided, all files are included.
  -x, --extensions EXTENSIONS
                        Comma-separated list of programming extensions to use. Replaces the default set if provided.
  -e, --exclude-dirs EXCLUDE_DIRS
                        Comma-separated list of directories to exclude. Replaces the default set if provided.
  -X, --exclude-extensions EXCLUDE_EXTENSIONS
                        Comma-separated list of file extensions to exclude from aggregation.
```

## Exclusions

The **All Code Aggregator** script automatically excludes specific directories and files to streamline the aggregation process and avoid including unnecessary or sensitive information.

### Excluded Directories

The following directories are excluded by default:

- `venv`
- `.venv`
- `node_modules`
- `__pycache__`
- `.git`
- `dist`
- `build`
- `temp`
- `old_files`
- `flask_session`

**Purpose**: These directories are typically used for virtual environments, dependencies, build artifacts, version control, or temporary files that are not part of the core codebase.

### Excluded Extensions

Users can now exclude specific file extensions using the `-X` or `--exclude-extensions` argument.

**Example:**
```bash
all-code -X .json,.md,.html
```
This will exclude all .json, .md, and .html files from aggregation.

## Example Output to full_code.txt
```
Directory Tree:
all_code/
│   ├── full_code.txt
│   ├── README.md
│   ├── test.py
│   ├── .git/ [EXCLUDED]
│   ├── demo_folder/
│   │   ├── another_file.js




# ======================
# File: test.py
# ======================

def greet(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet("World"))
    def farewell(name):
        return f"Goodbye, {name}!"

    print(farewell("World"))

# ======================
# File: demo_folder\another_file.js
# ======================

// another_file.js

// Function to add two numbers
function add(a, b) {
    return a + b;
}

// Function to subtract two numbers
function subtract(a, b) {
    return a - b;
}

// Function to multiply two numbers
function multiply(a, b) {
    return a * b;
}

// Function to divide two numbers
function divide(a, b) {
    if (b === 0) {
        throw new Error("Division by zero is not allowed.");
    }
    return a / b;
}

// Example usage
console.log("Add: " + add(5, 3));         // Output: Add: 8
console.log("Subtract: " + subtract(5, 3)); // Output: Subtract: 2
console.log("Multiply: " + multiply(5, 3)); // Output: Multiply: 15
console.log("Divide: " + divide(5, 3));     // Output: Divide: 1.6666666666666667
```


## Testing the script

If you want to test the script, run the following command.

```bash
python test_all_code.py
```

As of the current commit, only the command line args and their effects were tested, but more tests can be added in the future.
