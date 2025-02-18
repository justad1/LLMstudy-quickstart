import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from zhipuai import ZhipuAI
from zhipuai.core._errors import APIRequestFailedError

# 添加父目录到系统路径
root_dir = str(Path(__file__).resolve().parents[2])
if root_dir not in sys.path:
    sys.path.append(root_dir)

from ai_translator.model.model import Model

class GLMModel(Model):
    def __init__(self):
        load_dotenv()
        self.client = ZhipuAI(api_key=os.getenv("CHATGLM_API_KEY"))

    def make_request(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="glm-4",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content, True
        except APIRequestFailedError as e:
            raise Exception(f"API请求失败: {e}")
        except Exception as e:
            raise Exception(f"发生未知错误: {e}")

if __name__ == '__main__':
    model = GLMModel()
    response, success = model.make_request("你好")
    print(f"响应: {response}\n成功: {success}")
