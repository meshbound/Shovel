class ScriptGenerator:
    def generate_script(self, tags: list[str]) -> str:
        print("Generating script...")
        with open('src/generation/script_gen/test_script.txt', 'r') as file:
            return file.read()