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

class KimiModel(Model):
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(
            api_key=os.getenv("MOONSHOT_API_KEY"),
            base_url="https://api.moonshot.cn/v1"
        )

    def make_request(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            return response.choices[0].message.content, True
        except Exception as e:
            raise Exception(f"发生未知错误: {e}")

