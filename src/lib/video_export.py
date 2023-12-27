from lib.config import get_config
from lib.util import get_subdir_path
from moviepy.editor import VideoFileClip

def write_and_upload_video(video: VideoFileClip):
    path = write_video(video, get_config())
    upload_video(path)

def upload_video():
    print("Uploading video...")
    raise NotImplementedError

def write_video(video: VideoFileClip):
    name = "out.mp4"
    dest_path = get_subdir_path(get_config(), "video_out")
    video.write_videofile(f"{dest_path}/{name}",fps=24)