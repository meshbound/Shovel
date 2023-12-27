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
    for dir in config["dirs"]:
        for subdir in config["dirs"][dir]:
            if subdir == target:
                return config["dirs"][dir]["root"] + config["dirs"][dir][subdir]
    return None

def get_unix_time_millis() -> int:
    return int(time.time() * 1000)