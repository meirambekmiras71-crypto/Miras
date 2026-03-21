import shutil
import os

backup_filename = "data_backup.txt"

shutil.copy("data.txt", backup_filename)

if os.path.exists(backup_filename):
    with open(backup_filename, "r") as file:
        print(file.read())

if os.path.exists("data.txt"):
    os.remove("data.txt")

if os.path.exists(backup_filename):
    os.remove(backup_filename)