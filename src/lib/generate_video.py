from lib.generate_script import ScriptGenerator
import lib.script_parser as script_parser
from lib.video_outline import VideoOutline

async def generate_video(tags: list[str]) -> VideoOutline:
    script_generator = ScriptGenerator(use_placeholder=True)
    script = await script_generator.generate_script(tags)
    shot_outline = script_parser.parse_text(script)
    video_outline = await VideoOutline.generate(shot_outline)

    return video_outline