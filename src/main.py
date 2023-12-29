import asyncio
from lib.config import load_config
from lib.generate_video import generate_video
from lib.video_patcher import patch_video
from lib.video_export import VideoExporter

load_config()

async def create_video(tags):
    outline = await generate_video(tags)
    video = patch_video(outline)
    print(outline)

    video_exporter = VideoExporter(do_not_upload=True)
    video_exporter.write_and_upload_video(video, outline, tags)

if __name__ == "__main__":
    asyncio.run(create_video(["minecraft", "building", "zombies"]))