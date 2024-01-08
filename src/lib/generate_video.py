from lib.generate_script import ScriptGenerator
from lib.config import get_config
import lib.script_parser as script_parser
from lib.video_outline import VideoOutline

async def generate_video(tags: list[str]) -> VideoOutline:
    if len(tags) == 0:
        raise ValueError("Must provide at least one tag")
    
    use_placeholder = (get_config()["text_gen"]["use_placeholder"] == "True")
    script_generator = ScriptGenerator(use_placeholder)
    script = await script_generator.generate_script(tags)
    shot_outline = script_parser.parse_text(script)
    video_outline = await VideoOutline.generate(shot_outline)

    return video_outline