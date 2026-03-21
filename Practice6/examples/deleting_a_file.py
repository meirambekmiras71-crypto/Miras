import os

file_to_delete = "sample_backup.txt"

if os.path.exists(file_to_delete):
    os.remove(file_to_delete)