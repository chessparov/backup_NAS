from datetime import datetime
import os


def folder_size(path='.'):
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += folder_size(entry.path)
    return total


def nas_size(nas_letter: str):

    total = 0
    target_dirs = [
        # nas_letter + ":\\" + "Documenti",
                   nas_letter + ":\\" + "Immagini",
    #                nas_letter + ":\\" + "Video"
                   ]
    for directory in target_dirs:
        total += folder_size(directory)

    return total


def disk_size(drive_letter: str):

    today_date = datetime.today().date()
    target_dir = drive_letter + r":\Backup_" + today_date.strftime('%d_%m_%Y')
    total = folder_size(target_dir)

    return total
