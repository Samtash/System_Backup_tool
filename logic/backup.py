import os

from logic.versioning import create_backup_folder
from utilis.file_utilis import get_all_files, copy_file




 
def run_backup(source_folder: str,
               dest_root: str,
               log_callback,
               status_callback,
               progress_callback):
    """
    Perform a FULL backup:
    - Create a new version folder inside dest_root
    - Copy all files from source_folder into that version folder
      (preserving folder structure)
    - Update UI via callbacks.
    """

    status_callback("Creating version folder...")
    version_folder = create_backup_folder(dest_root)
    log_callback(f"Created version folder: {version_folder}")

    # 1) Collect all files from source
    files = get_all_files(source_folder)
    total = len(files)

    if total == 0:
        log_callback("No files found in source folder.")
        status_callback("Backup finished (nothing to copy).")
        progress_callback(100)
        return

    status_callback("Copying files...")
    copied = 0

    # 2) Copy each file
    for idx, src_path in enumerate(files, start=1):
        # keep relative structure
        rel_path = os.path.relpath(src_path, source_folder)
        dst_path = os.path.join(version_folder, rel_path)

        copy_file(src_path, dst_path)
        copied += 1
        log_callback(f"Copied: {src_path} -> {dst_path}")

        # update progress (0–100)
        progress = int(idx * 100 / total)
        progress_callback(progress)

    status_callback(f"Backup completed. Files copied: {copied}")
    log_callback("=== Backup completed successfully ===")
