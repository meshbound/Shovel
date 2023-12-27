from lib.config import get_config
from configobj import ConfigObj
from openai import OpenAI

class ScriptGenerator:
    def __init__(self, use_placeholder: bool = False):
        self.use_placeholder = use_placeholder
        if use_placeholder:
            return
        self._text_gen_config: dict = get_config()["text_gen"]
        self._client = OpenAI(
            api_key=self._text_gen_config["api_key"],
        )

    def generate_script(self, tags: list[str]) -> str:
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
        return response.choices[0].message.content