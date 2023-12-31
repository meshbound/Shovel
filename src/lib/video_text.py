from lib.util import get_subdir_path, get_unix_time_millis
from lib.config import get_config
from moviepy.editor import ImageClip
import imgkit

def text_to_image(
        text: str, 
        font_size: int = 50, 
        font_name: str = "Arial",
        font_color: str = "white",
        outline_ratio: float = 0.2,
        outline_color: str = "black"
        ) -> ImageClip:

    body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            h2 {{
                font: 800 {font_size}px {font_name};
                color: {outline_color};
                text-align: center;
                padding: 70px 0;
                inline-size: 1080px;
                overflow-wrap: break-word;
                -webkit-text-fill-color: {font_color};
                -webkit-text-stroke: {font_size * outline_ratio}px {outline_color};
            }}
        </style>
    </head>
    <body>
        <h2>{text}</h2>
    </body>
    </html>"""
    options = {
        "transparent": "",
    }

    filename = get_unix_time_millis()
    base_path = get_subdir_path(get_config(), "text_temp")
    file_path = f"{base_path}/{filename}.png"
    imgkit.from_string(string=body, output_path=file_path, options=options)
    return ImageClip(file_path)
