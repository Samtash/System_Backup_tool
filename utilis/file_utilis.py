import os
import shutil


def get_all_files(root_folder: str):
    """
    Walk through root_folder and return a list of full file paths.
    """
    file_paths = []
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for name in filenames:
            full_path = os.path.join(dirpath, name)
            file_paths.append(full_path)
    return file_paths


def ensure_parent_dir(path: str):
    """
    Make sure the parent directory of 'path' exists.
    """
    parent = os.path.dirname(path)
    os.makedirs(parent, exist_ok=True)


def copy_file(src: str, dst: str):
    """
    Copy a file from src to dst, creating parent folders if needed.
    Uses copy2 to preserve metadata (timestamps etc.).
    """
    ensure_parent_dir(dst)
    shutil.copy2(src, dst)
