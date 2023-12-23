from lib.generate_script import ScriptGenerator
from lib.script_parser import parse_text
from lib.video_outline import VideoOutline

def generate_video(tags: list[str]) -> VideoOutline:
    script_generator = ScriptGenerator()
    script = script_generator.generate_script(tags, use_placeholder=True)
    shot_outline = parse_text(script)
    video_outline = VideoOutline.generate(shot_outline)

    return video_outline