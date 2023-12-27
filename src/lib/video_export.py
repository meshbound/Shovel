import time
from lib.config import get_config
from lib.util import get_subdir_path, get_unix_time_millis
from moviepy.editor import VideoFileClip

def write_and_upload_video(video: VideoFileClip):
    path = write_video(video, get_config())
    upload_video(path)

def upload_video():
    print("Uploading video...")
    raise NotImplementedError

def write_video(video: VideoFileClip):
    filename = get_unix_time_millis()
    dest_path = get_subdir_path(get_config(), "video_out")
    file_path = f"{dest_path}/{filename}.mp4"
    fps = float(get_config()["video"]["framerate"])
    video.write_videofile(file_path, fps=fps)