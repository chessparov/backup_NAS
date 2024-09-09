import string
from ctypes import windll
import shutil

def get_drives():
    drives = ["Seleziona unità"]
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            available_space = round(shutil.disk_usage(letter + ":\\").free / 1073741824, 1) # From bytes to Gibibytes
            drives.append(letter + ":   Spazio Disponibile [" + str(available_space) + " GB]")
        bitmask >>= 1

    return drives
