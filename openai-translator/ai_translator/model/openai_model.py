import os
import sys
import time
import openai
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# 添加父目录到系统路径
root_dir = str(Path(__file__).resolve().parents[2])
if root_dir not in sys.path:
    sys.path.append(root_dir)

from ai_translator.model.model import Model
from ai_translator.utils import LOG

class OpenAIModel(Model):
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.max_retries = 3
        self.retry_delay = 60

    def make_request(self, prompt):
        attempts = 0
        while attempts < self.max_retries:
            try:
                if self.model == "gpt-3.5-turbo":
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    return response.choices[0].message.content.strip(), True
                else:
                    response = self.client.completions.create(
                        model=self.model,
                        prompt=prompt,
                        max_tokens=150,
                        temperature=0
                    )
                    return response.choices[0].text.strip(), True

            except openai.RateLimitError as e:
                attempts += 1
                if attempts < self.max_retries:
                    LOG.warning(f"速率限制达到，等待 {self.retry_delay} 秒后重试。")
                    time.sleep(self.retry_delay)
                else:
                    raise Exception("达到速率限制。超过最大重试次数。")

            except openai.APIConnectionError as e:
                raise Exception(f"无法连接到服务器: {e.__cause__}")

            except openai.APIStatusError as e:
                raise Exception(f"API 返回非 200 状态码: {e.status_code}, 响应: {e.response}")

            except Exception as e:
                raise Exception(f"发生未知错误: {e}")

        return "", False


