import os
import argparse
import sys
import subprocess

FULL_CODE_FILE_NAME = "full_code.txt"
FILES_TO_INCLUDE = set()
EXCLUDE_EXTENSIONS = set()

PROGRAMMING_EXTENSIONS = {
    '.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.c', '.cpp', '.html', '.css',
    '.json', '.toml', '.yml', '.yaml', '.ini', '.sql', '.sh', '.bat', '.ps1'
}

EXCLUDE_DIRS = {
    'venv', '__pycache__', '.git', '.venv', 'node_modules', '.ipynb_checkpoints'
}

SCRIPT_NAME = os.path.basename(__file__)
EXCLUDE_FILES = {SCRIPT_NAME, FULL_CODE_FILE_NAME}


def is_programming_file(filename):
    _, ext = os.path.splitext(filename)
    return ext.lower() in PROGRAMMING_EXTENSIONS and ext.lower() not in EXCLUDE_EXTENSIONS


def should_exclude(path):
    norm = os.path.normpath(path)
    parts = norm.split(os.sep)
    if any(part in EXCLUDE_DIRS for part in parts[:-1]):
        return True
    if parts[-1] in EXCLUDE_FILES:
        return True
    return False


def should_include_file(path):
    return True if not FILES_TO_INCLUDE else os.path.relpath(path) in FILES_TO_INCLUDE


def generate_directory_tree(startpath):
    tree = []
    for root, dirs, files in os.walk(startpath):
        rel_path = os.path.relpath(root, startpath)
        if rel_path == '.':
            rel_path = ''
        depth = len(rel_path.split(os.sep)) if rel_path else 0
        indent = '│   ' * depth + '├── ' if depth > 0 else ''
        dirname = os.path.basename(root) if rel_path else os.path.basename(startpath.rstrip(os.sep)) or startpath

        if dirname in EXCLUDE_DIRS:
            tree.append(f"{indent}{dirname}/ [EXCLUDED]")
            dirs[:] = []
            continue

        tree.append(f"{indent}{dirname}/")
        for f in files:
            if f in EXCLUDE_FILES:
                continue
            tree.append(f"{'│   ' * (depth + 1)}├── {f}")
    return '\n'.join(tree)


def copy_to_clipboard(content):
    try:
        if os.name == 'nt':
            cmd = 'clip'
        elif sys.platform == 'darwin':
            cmd = 'pbcopy'
        else:
            cmd = 'xclip -selection clipboard'
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True)
        process.communicate(content.encode('utf-8'))
        return True
    except Exception as e:
        print(f"Clipboard error: {e}")
        return False


def parse_arguments():
    parser = argparse.ArgumentParser(description="Aggregate source files into one master file with a directory tree.")
    parser.add_argument('-d', '--directory', type=str, default=os.getcwd(),
                        help="Directory to scan (default: current directory).")
    parser.add_argument('-o', '--output-file', type=str, default=FULL_CODE_FILE_NAME,
                        help="Output filename (default: full_code.txt).")
    parser.add_argument('-i', '--include-files', type=str, default="",
                        help="Comma-separated list of files to include explicitly.")
    parser.add_argument('-x', '--extensions', type=str, default="",
                        help="Comma-separated list of extensions to include (overrides defaults).")
    parser.add_argument('-X', '--exclude-extensions', type=str, default="",
                        help="Comma-separated list of extensions to exclude.")
    parser.add_argument('-c', '--clipboard', action='store_true',
                        help="Copy output to clipboard instead of file.")
    return parser.parse_args()


def main():
    args = parse_arguments()

    global FULL_CODE_FILE_NAME, EXCLUDE_EXTENSIONS, PROGRAMMING_EXTENSIONS, FILES_TO_INCLUDE
    FULL_CODE_FILE_NAME = args.output_file

    if args.include_files:
        FILES_TO_INCLUDE = {f.strip() for f in args.include_files.split(',') if f.strip()}

    if args.extensions:
        PROGRAMMING_EXTENSIONS = {ext if ext.startswith('.') else f'.{ext}' for ext in args.extensions.split(',')}

    if args.exclude_extensions:
        EXCLUDE_EXTENSIONS = {ext if ext.startswith('.') else f'.{ext}' for ext in args.exclude_extensions.split(',')}

    startpath = os.path.normpath(args.directory)
    if not os.path.isdir(startpath):
        print(f"Error: Directory not found: {startpath}")
        sys.exit(1)

    print(f"📁 Scanning: {startpath}")
    print(f"📦 Extensions included: {PROGRAMMING_EXTENSIONS or '[ALL]'}")
    print(f"🚫 Extensions excluded: {EXCLUDE_EXTENSIONS or '[NONE]'}")

    print("🧱 Generating directory tree...")
    directory_tree = generate_directory_tree(startpath)
    aggregated = [f"Directory Tree:\n{directory_tree}\n\n"]

    count = 0
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.normpath(os.path.relpath(file_path, startpath))
            if should_exclude(rel_path):
                continue
            if not should_include_file(file_path):
                continue
            if not is_programming_file(file):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    header = f"\n\n# ======================\n# File: {rel_path}\n# ======================\n\n"
                    aggregated.append(header + content)
                    count += 1
            except Exception as e:
                aggregated.append(f"\n# Error reading {rel_path}: {e}")

    result = '\n'.join(aggregated)

    if args.clipboard:
        success = copy_to_clipboard(result)
        if success:
            print(f"📋 Copied {count} files to clipboard.")
        else:
            print("❌ Clipboard copy failed.")
            sys.exit(1)
    else:
        try:
            with open(FULL_CODE_FILE_NAME, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"✅ Written {count} files to {FULL_CODE_FILE_NAME}")
        except Exception as e:
            print(f"❌ Failed to write file: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
