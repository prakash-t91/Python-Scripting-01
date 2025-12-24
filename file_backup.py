#!/usr/bin/env python3
#############################################
#Script Name: file_backup.py
#Description: Creates a backup of the current directory, excluding virtual environment folders.
# Author: Prakash T P
#Date: 2024-06-15
#Version: 1.0
#############################################

import os
import datetime
import shutil
from shutil import copytree, ignore_patterns

src_dir = "./"
dst_dir = "/home/$USER/backups"
archive_name = "Backup_"
IGNORE_PATTERNS = ('.venv', 'venv') 

home_dir = os.environ['HOME'] 
dirname = os.path.join(home_dir, "Backups/")

if os.path.isdir(dirname) == False:
    os.makedirs(dirname, exist_ok=True)
    os.chmod(dirname, 0o777)
    print("%s directory has been created." % dirname)
else:
    print("The directory already exists.")
    
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
dst_dir = os.path.join(dirname + archive_name + timestamp)

shutil.copytree(src_dir, dst_dir, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))
shutil.make_archive(dst_dir, 'zip', dst_dir)
shutil.rmtree(dst_dir)
print("Backup created successfully at:", dst_dir)
