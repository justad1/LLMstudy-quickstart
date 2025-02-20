import os
import sys
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# 添加父目录到系统路径
root_dir = str(Path(__file__).resolve().parents[2])
if root_dir not in sys.path:
    sys.path.append(root_dir)

from ai_translator.model.model import Model

class DeepseekModel(Model):
    def __init__(self, config=None):
        self.client = OpenAI(
            api_key=config.get('deepseek_api_key') if config else os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )

    def make_request(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                stream=False
            )
            return response.choices[0].message.content, True
        except Exception as e:
            raise Exception(f"发生未知错误: {e}")

