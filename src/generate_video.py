from generation.script_gen.generate_script import ScriptGenerator
from generation.script_gen.parser import parse_text
from generation.script_gen.outline import VideoOutline
from generation.media_gen.video_outline import generate_video_outline
from PIL import Image

def generate_video(tags: list[str]) -> VideoOutline:
    script_generator = ScriptGenerator()
    script = script_generator.generate_script(tags)
    shot_outline = parse_text(script)
    video_outline = generate_video_outline(shot_outline)

    # shot = video_outline.shots[0]
    # print(f"Shot: {shot.text}")
    # print(f"Speech: {shot.speech}")
    # print(f"Image: {shot.image}")

    return video_outline