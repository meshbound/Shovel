from lib.config import get_config
from lib.util import get_subdir_path, get_files_in_dir, get_unix_time_millis
from lib.video_outline import VideoOutline
from moviepy.editor import VideoFileClip
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

class VideoExporter:
    def __init__(self, do_not_upload: bool = False):
        self.do_not_upload = do_not_upload
        if do_not_upload:
            return
        auth_path = get_subdir_path(get_config(), "youtube")
        secret_files = get_files_in_dir(auth_path, ".json")
        credential_files = get_files_in_dir(auth_path, ".storage")
        if len(secret_files) == 0:
            raise Exception("[Video export] No Youtube auth file found")
        secret_path = f"{auth_path}/{secret_files[0]}"
        credential_path = (f"{auth_path}/{'credential.storage'}"
                           if len(credential_files) == 0 
                           else f"{auth_path}/{credential_files[0]}")
        self.client = Channel()
        self.client.login(secret_path, credential_path)

    def write_and_upload_video(self, video: VideoFileClip, outline: VideoOutline, tags: list[str] = []):
        path = self.write_video(video)
        self.upload_video(path, outline, tags)
 
    def upload_video(self, video_path: str, outline: VideoOutline, tags: list[str] = []) -> bool:
        if self.do_not_upload:
            return
        print("Uploading video...")
        video = LocalVideo(file_path=video_path)
        
        include_generation_tags = bool(get_config()["upload"]["include_generation_tags"])
        if not include_generation_tags:
            tags = []
        p_tags = get_config()["upload"]["persistent_tags"]
        tags.extend([
            tag for tag in p_tags.strip().split(",")
        ])
        tags = [f"#{tag.strip().replace('#','')}"
                for tag in tags]

        default_language = get_config()["upload"]["default_language"]
        embeddable = bool(get_config()["upload"]["embeddable"])
        visibility = get_config()["upload"]["visibility"]
        public_stats = bool(get_config()["upload"]["public_stats"])

        video.set_title(outline.title)
        video.set_description(outline.description)
        video.set_tags(tags)
        video.set_default_language(default_language)
        video.set_embeddable(embeddable)
        video.set_privacy_status(visibility)
        video.set_public_stats_viewable(public_stats)

        try:
            video = self.client.upload_video(video)
        except:
            print("[Video export] Youtube API quota exceeded!")
            return False

        video_url = f"https://www.youtube.com/watch?v={video.id}"
        print(f"Video live on youtube: {video_url}")
        return True
            

    @staticmethod
    def write_video(video: VideoFileClip) -> str:
        filename = get_unix_time_millis()
        dest_path = get_subdir_path(get_config(), "video_out")
        file_path = f"{dest_path}/{filename}.mp4"
        fps = float(get_config()["video"]["framerate"])
        video.write_videofile(file_path, fps=fps)
        return file_path