import random
import numpy
import hashlib
import lib.config as config
from PIL import Image
from PIL import ImageDraw, ImageFont
from moviepy.editor import ImageClip
from openai import OpenAI

class ImageGenerator:
    def __init__(self):
        self._text_gen_config: dict = config.get_value("text_gen")
        self._client = OpenAI(
            api_key=self._text_gen_config.get("api_key"),
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

    def generate_image(self, prompt: str, use_placeholder: bool = False) -> ImageClip:
        print(f"Generating image from prompt: {prompt}")

        if use_placeholder:
            return ImageGenerator.__generate_placeholder_image(prompt)
        
        response = self._client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="512x512",
            n=1
        )
        image_url = response.data[0].url
        print("Generated image: " + image_url)