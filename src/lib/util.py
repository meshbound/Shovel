from configobj import ConfigObj
import random
import os
import time

def get_files_in_dir(dir_path: str) -> list[str]:
    files = [f for f in os.listdir(dir_path) 
             if os.path.isfile(f"{dir_path}/{f}")]
    return files

def random_file_from_dir(dir_path: str) -> str:
    files = get_files_in_dir(dir_path)
    if len(files) == 0:
        return None
    file_select = files[random.randint(0, len(files) - 1)]
    return file_select

def get_subdir_path(config: ConfigObj, target: str) -> str:
    if target == "root":
        return None
    dirs = config["dirs"]
    for dir in dirs:
        subdirs = config["dirs"][dir]
        for subdir in subdirs:
            if subdir == target:
                return subdirs["root"] + subdirs[subdir]
    return None

def get_unix_time_millis() -> int:
    return int(time.time() * 1000)