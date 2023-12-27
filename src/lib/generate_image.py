import random
import numpy
import hashlib
import math
import time
import urllib.request
from lib.config import get_config
from lib.util import get_subdir_path, get_unix_time_millis
from lib.stability.api import StabilityAPI
from configobj import ConfigObj
from PIL import Image
from PIL import ImageDraw, ImageFont
from moviepy.editor import ImageClip
# from lib.stability.api import StabilityAPI

class ImageGenerator:
    def __init__(self, use_placeholder: bool = False):
        self.use_placeholder = use_placeholder
        if use_placeholder:
            return
        self._image_gen_config: ConfigObj = get_config()["image_gen"]
        self._client = StabilityAPI(
            api_key=self._image_gen_config["api_key"],
        )

    @staticmethod
    def __generate_placeholder_image(prompt: str) -> ImageClip:
        prompt_hash = hashlib.sha256(prompt.encode()).digest()
        seeded_random = random.Random(prompt_hash)

        red = seeded_random.randint(0, 255)
        green = seeded_random.randint(0, 255)
        blue = seeded_random.randint(0, 255)
        color = (red, green, blue)

        image = Image.new('RGB', (512, 512), color)
        image_draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 24)
        y = 10
        for _ in range(15):
            image_draw.text((11, y+1), prompt, fill=(0, 0, 0), font=font)
            image_draw.text((10, y), prompt, fill=(255, 255, 255), font=font)
            y += 30

        return ImageClip(numpy.array(image))

    async def generate_image(self, prompt: str) -> ImageClip:
        print(f"Generating image from prompt: {prompt}")

        if self.use_placeholder:
            return ImageGenerator.__generate_placeholder_image(prompt)
        
        width = self._image_gen_config["width"]
        height = self._image_gen_config["height"]
        image = await self._client.text_to_image(
            prompt=prompt,
        )
        return image

    @staticmethod
    def __download_image(image_url: str) -> ImageClip:
        filename = get_unix_time_millis()
        base_path = get_subdir_path(get_config(), "image_temp")
        file_path = f"{base_path}/{filename}.png"
        urllib.request.urlretrieve(image_url, file_path)
        return ImageClip(file_path)