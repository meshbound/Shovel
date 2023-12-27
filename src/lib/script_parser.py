import re
from lib.video_outline import ShotOutline, ShotOutlineMeta

class ScriptTag:
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content

def parse_tag(text: str) -> ScriptTag:
    match = re.search(r"\[(\w+)(.*)\]", text)
    if match is None:
        return None
    tag = match.group().strip().split(":")
    name = tag[0][1:].strip()
    content = tag[1][:-1].strip()
    # print("Tag:", name, content)
    return ScriptTag(name, content)
    
def parse_shot(text: str) -> ShotOutline:
    lines = text.strip().split('\n')
    text = lines[0].strip()
    prompt = parse_tag(lines[1]).content
    return ShotOutline(text, prompt)

def parse_text(text: str) -> ShotOutlineMeta:
    shots_text: list[str] = text.split('\n\n')

    meta = shots_text[0].split('\n')
    title: str = None
    description: str = None
    tags: list[ScriptTag] = []
    for tag in meta:
        tag = parse_tag(tag)
        if tag.name == "title":
            title = tag.content
        elif tag.name == "description":
            description = tag.content

    shots: list[ShotOutline] = []
    for shot_text in shots_text[1:]:
        print(shot_text)
        shots.append(parse_shot(shot_text))
    
    shot_outline_meta = ShotOutlineMeta(title, description, shots)
    return shot_outline_meta