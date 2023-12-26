from moviepy.editor import VideoFileClip
from config import get_config

def write_and_upload_video(video: VideoFileClip):
    path = write_video(video, get_config())
    upload_video(path)

def upload_video():
    print("Uploading video...")
    raise NotImplementedError

def write_video(video: VideoFileClip):
    name = "out.mp4"
    dest_path = get_config()["dirs"]["root"] + get_config()["dirs"]["sub_dirs"]["video_out"]
    video.write_videofile(dest_path + "/" + name,fps=24)