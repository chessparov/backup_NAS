import os
import shutil
import datetime


def create_backup(drive_letter: str, nas_letter: str):
    today_date = datetime.datetime.today().date()
    backup_directory = drive_letter + r":\Backup_" + today_date.strftime('%d_%m_%Y')
    if not os.path.exists(backup_directory):
        os.mkdir(backup_directory)

    nas_documenti = nas_letter + ":\\" + "Documenti"
    nas_immagini = nas_letter + ":\\" + "Immagini"
    nas_video = nas_letter + ":\\" + "Video"
    nas_programmi = nas_letter + ":\\" + "Programmi"

    drive_documenti = backup_directory + "\\Documenti"
    drive_immagini = backup_directory + "\\Immagini"
    drive_video = backup_directory + "\\Video"
    drive_programmi = backup_directory + "\\Programmi"

    # try:
    if os.path.exists(nas_documenti):
        shutil.copytree(nas_documenti, drive_documenti, dirs_exist_ok=True)
# except PermissionError:
#     print("Permission Denied: " + nas_documenti)
# try:
    if os.path.exists(nas_immagini):
        shutil.copytree(nas_immagini, drive_immagini, dirs_exist_ok=True)
# except PermissionError:
#     print("Permission Denied: " + nas_immagini)
# try:
    if os.path.exists(nas_video):
        shutil.copytree(nas_video, drive_video, dirs_exist_ok=True)
# except PermissionError:
#     print("Permission Denied: " + nas_video)
# try:
    if os.path.exists(nas_programmi):
        shutil.copytree(nas_programmi, drive_programmi, dirs_exist_ok=True)
    # except PermissionError:
    #     print("Permission Denied: " + nas_programmi)

    return
