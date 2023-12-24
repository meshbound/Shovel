from configobj import ConfigObj
from moviepy.editor import ImageClip
from PIL import Image
import numpy
import os

def get_files_in_dir(dir_path: str):
    files = [f for f in os.listdir(dir_path) 
             if os.path.isfile(dir_path + "/" + f)]
    return files

def get_subdir_path(config: ConfigObj, subfolder: str):
    return config["dirs"]["root"] + config["dirs"]["sub_dirs"][subfolder]

def to_imageclip(image: Image):
    return ImageClip(numpy.array(image))