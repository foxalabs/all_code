# All Code Aggregator

## Overview

The **All Code Aggregator** script consolidates all programming-related code files in the current directory into a single `full_code.txt` file. This is especially useful for providing your entire codebase to AI models for analysis or assistance.

## Features

- **Directory Tree Generation**: Creates an ASCII representation of the directory structure, excluding specified directories.
- **Code Aggregation**: Combines contents of programming-related files into a master file.
- **Customizable Inclusions/Exclusions**: Easily specify which files or directories to include or exclude.

## Setup

### Using UV (Recommended)

Since All Code Aggregator is better used as a command-line interface, installing with [uv](https://docs.astral.sh/uv/) makes `all-code` command automatically available system wide without interfering with the system python or with virtual environments.

1. **Install uv**

Use the one line standalone installer from uv's [docs page](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer).

2. **Install All Code Aggregator CLI from github source**

```
uv tool install git+https://github.com/hermesribeiro/all_code@0.1.0
```

3. **Use it in your project**

```
# Run the CLI command to generate the Aggregated code.
all-code
# Shell output:
# Full code file 'full_code.txt' has been created successfully.
```


### Using venv+pip

A python native method of installing. Requires an activated virtualenv to be used.

1. **Install it in a virtualenv using pip**

```
# Create a virtual environment
python3 -m venv venv
# Activate the virtual environment
source venv/bin/activate
# Install the package
pip install git+https://github.com/hermesribeiro/all_code@0.1.0
```

2. **Use it in your project**

```
# Run the CLI command to generate the Aggregated code.
all-code
# Shell output:
# Full code file 'full_code.txt' has been created successfully.
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

**Example Output to full_code.txt**
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
