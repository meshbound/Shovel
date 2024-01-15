import asyncio
from lib.config import load_config, get_config
from lib.generate_video import generate_video
from lib.video_patcher import patch_video
from lib.util import clean_dirs, parse_tags
from lib.args import get_args
from lib.video_export import VideoExporter

load_config()
if get_config()["video"]["last_temp_only"] == "True":
    clean_dirs(get_config(), [("audio_temp",".wav"),("audio_temp",".mp3"),("image_temp",".png"),
                              ("script_temp",".txt"),("caption_temp",".png")])

async def create_video(tags, mode):
    outline = await generate_video(tags)
    video = patch_video(outline)
    do_not_upload = (get_config()["upload"]["do_not_upload"] == "True")
    video_exporter = VideoExporter(do_not_upload)

    if mode == "gen_only":
        video_exporter.write_video(video)
    elif mode == "gen_and_upload":
        video_exporter.write_and_upload_video(video, outline, tags)

if __name__ == "__main__":
    args = get_args()
    asyncio.run(create_video(parse_tags(args.tags), args.mode))
