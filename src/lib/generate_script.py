from lib.util import get_unix_time_millis
from lib.config import get_config, get_subdir_path
from configobj import ConfigObj
from openai import OpenAI

class ScriptGenerator:
    def __init__(self, use_placeholder: bool = False):
        self.use_placeholder = use_placeholder
        if use_placeholder:
            return
        self._text_gen_config: dict = get_config()["text_gen"]
        config_api_key = self._text_gen_config["api_key"]
        if config_api_key is None:
            raise Exception("[Text generation] OpenAI API key not set")
        self._client = OpenAI(
            api_key=self._text_gen_config["api_key"],
        )

    async def generate_script(self, tags: list[str]) -> str:
        print("Generating script...")

        if len(tags) == 0:
            raise ValueError("Must provide at least one tag")
        
        if self.use_placeholder:
            with open("src/lib/placeholder_script.txt", "r") as f:
                return f.read()

        temperature = float(self._text_gen_config["temperature"])
        response = self._client.chat.completions.create(
            model=self._text_gen_config["model"],
            temperature=temperature,
            # max_length=_text_gen_config.get("max_length"),
            messages=[
                {
                    "role": "system",
                    "content": self._text_gen_config["prompt"]
                },
                {
                    "role": "user",
                    "content": f"Prompt: {', '.join(tags)}"
                }
            ],
        )
        script = response.choices[0].message.content
        filename = get_unix_time_millis()
        base_dir = get_subdir_path(get_config(), "text_temp")
        path = f"{base_dir}/{filename}.txt"
        with open(path, "w", encoding="utf-8") as f:
            f.write(script)
        return script