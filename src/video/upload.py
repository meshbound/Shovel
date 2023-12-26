from moviepy.editor import VideoFileClip
from configobj import ConfigObj
from os import path

def write_and_upload_video(config: ConfigObj, video: VideoFileClip):
    path = write_video(video, config)
    upload_video(path)

def upload_video():
    print("Uploading video...")
    raise NotImplementedError

def write_video(config: ConfigObj, video: VideoFileClip):
    name = "out.mp4"
    dest_path = config["dirs"]["root"] + config["dirs"]["sub_dirs"]["video_out"]
    video.write_videofile(dest_path + "/" + name,fps=24)