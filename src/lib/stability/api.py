import requests

class StabilityAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def __api_call(self, endpoint: str, method: str) -> dict:
        if self.api_key is None:
            raise Exception("API key not set")
        
        url = f"https://api.stability.ai/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = None
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers)

        if response.status_code != 200:
            raise Exception("API response error: " + str(response.text))

        return response.json()