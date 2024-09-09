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

    # if os.path.exists(nas_letter + ":\\" + "Video"):
    #     shutil.copytree(nas_video, drive_video)
    # if os.path.exists(nas_letter + ":\\" + "Documenti"):
    #     shutil.copytree(nas_documenti, drive_documenti)
    if os.path.exists(nas_letter + ":\\" + "Immagini"):
        shutil.copytree(nas_immagini, drive_immagini)
    # if os.path.exists(nas_programmi):
    #     shutil.copytree(nas_programmi, drive_programmi)

    return
