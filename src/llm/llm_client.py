from openai import OpenAI
from utils.config import DEEPSEEK_API_KEY, MODEL_NAME
from llm.prompts import SYSTEM_PROMPT

class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"
        )

    def generate_response(self, question, context):
        try:
            prompt = f"""
数据集信息：

{context}

用户问题：

{question}
"""
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3
            )
            return response.choices[0].message.content

        except Exception as e:
            return f"AI分析失败：{str(e)}"