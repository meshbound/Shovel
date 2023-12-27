import httpx
import base64
import math
import time
from moviepy.editor import ImageClip
from lib.config import get_config
from lib.util import get_subdir_path
from lib.stability.api_types import EngineListing

class StabilityAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def list_engines(self) -> list[EngineListing]:
        response = await self.__api_call("engines/list", "GET")
        engines = []
        for engine in response:
            engines.append(EngineListing(
                description=engine["description"],
                id=engine["id"],
                name=engine["name"],
                engine_type=engine["type"]
            ))
        return engines

    async def text_to_image(self, prompt: str, engine_id: str = "stable-diffusion-xl-1024-v1-0") -> list[ImageClip]:
        json = {
            "text_prompts": [
                { "text": prompt }
            ],
            "cfg_scale": 7,
            # "samples": 1,
            "steps": 30,
        }
        
        response = await self.__api_call(f"generation/{engine_id}/text-to-image", "POST", json)

        image = response["artifacts"][0]
        filename = math.floor(time.time() * 1000)
        base_path = get_subdir_path(get_config(), "image_temp")
        file_path = f"{base_path}/{filename}.png"
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(image["base64"]))
        return ImageClip(file_path)

    async def __api_call(self, endpoint: str, method: str, json: dict = None) -> dict:
        if self.api_key is None:
            raise Exception("API key not set")
        
        url = f"https://api.stability.ai/v1/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = None

        async with httpx.AsyncClient() as httpx_client:
            if method == "GET":
                response = await httpx_client.get(url, headers=headers, timeout=None)
            elif method == "POST":
                response = await httpx_client.post(url, headers=headers, json=json, timeout=None)

        if response.status_code != 200:
            raise Exception("API response error: " + str(response.text))

        return response.json()