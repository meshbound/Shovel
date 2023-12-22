from .outline import ShotOutline

def parse_shot(text: str) -> ShotOutline:
    lines = text.strip().split('\n')
    text = lines[0].strip()
    prompt = lines[1].replace("[img:", "").replace("]", "").strip()
    return ShotOutline(text, prompt)

def parse_text(text: str) -> list[ShotOutline]:
    shots_text: list[str] = text.split('\n\n')
    shots: list[ShotOutline] = []
    for shot_text in shots_text:
        shots.append(parse_shot(shot_text))
    return shots