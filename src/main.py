import asyncio
from lib.config import load_config
from lib.generate_video import generate_video
from lib.video_composer import patch_video
from lib.video_export import write_video

load_config()

async def create_video(tags):
    video = await generate_video(tags)
    patched = patch_video(video)
    write_video(patched)
    print(video)

if __name__ == "__main__":
    asyncio.run(create_video(["minecraft", "building", "zombies"]))