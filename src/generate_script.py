from .generation import config
from openai import ChatCompletion

class ScriptGenerator:
    def generate_script(self, tags: list[str]) -> str:
        print("Generating script...")
        response = ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Say this is a test"
                },
                {
                    "role": "user",
                    "content": "Say this is a test"
                }
            ],
        )