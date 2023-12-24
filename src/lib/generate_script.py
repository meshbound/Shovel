import lib.config as config
from openai import OpenAI

class ScriptGenerator:
    def __init__(self):
        self._text_gen_config: dict = config.get_value("text_gen")
        self._client = OpenAI(
            api_key=self._text_gen_config.get("api_key"),
        )

    def generate_script(self, tags: list[str], use_placeholder: bool = False) -> str:
        print("Generating script...")

        if len(tags) == 0:
            raise ValueError("Must provide at least one tag")
        
        if use_placeholder:
            with open("src/lib/placeholder_script.txt", "r") as f:
                return f.read()

        response = self._client.chat.completions.create(
            model=self._text_gen_config.get("model"),
            temperature=self._text_gen_config.get("temperature"),
            # max_length=_text_gen_config.get("max_length"),
            messages=[
                {
                    "role": "system",
                    "content": self._text_gen_config.get("prompt")
                },
                {
                    "role": "user",
                    "content": f"Prompt: {', '.join(tags)}"
                }
            ],
        )
        return response.choices[0].message.content