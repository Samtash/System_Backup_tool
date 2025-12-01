import os
from datetime import datetime


def create_backup_folder(dest_path):
    """
    Creates a new backup version folder inside the destination path.
    Returns the full path of the created folder.
    """

    # Create a timestamped folder name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = f"Backup_{timestamp}"

    full_path = os.path.join(dest_path, folder_name)

    # Create the folder
    os.makedirs(full_path, exist_ok=True)

    return full_path
