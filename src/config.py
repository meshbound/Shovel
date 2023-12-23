from configobj import ConfigObj
from os import path, mkdir

config_path = "./shovel.ini"

def load_config() -> ConfigObj:
    if not path.exists(config_path):
        print("No config found!")
        write_default_config()
    config = ConfigObj(config_path)
    verify_file_structure(config)
    return config

def write_default_config():
    print("Writing new config...")
    config = ConfigObj()
    config.filename = config_path

    config["dirs"] = {}
    dirs = config["dirs"]
    dirs["root"] = "./out/"
    dirs["sub_dirs"] = {}
    sub_dirs = dirs["sub_dirs"]
    sub_dirs["video_out"] = "video"
    
    config.write()

def verify_file_structure(config: ConfigObj):
    root = config["dirs"]["root"]
    if not path.exists(root):
        mkdir(root)
    sub_dirs = config["dirs"]["sub_dirs"]
    for sub_dir in sub_dirs:
        dir_path = root + sub_dirs[sub_dir]
        if not path.exists(dir_path):
            mkdir(dir_path)