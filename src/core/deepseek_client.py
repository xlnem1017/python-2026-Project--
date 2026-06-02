import requests
from utils.config import DEEPSEEK_API_KEY

class DeepSeekClient:

    BASE_URL = "https://api.deepseek.com/v1"

    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY

    def analyze_dataframe(self, df, task="summary"):
        data = {
            "task": task,
            "data": df.to_dict(orient="records")
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(f"{self.BASE_URL}/analyze", json=data, headers=headers)
        response.raise_for_status()
        return response.json()