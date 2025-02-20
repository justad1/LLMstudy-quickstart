from dotenv import load_dotenv
import os
import sys
import pathlib

# 添加项目根目录到Python路径
root_dir = str(pathlib.Path(__file__).parent.parent.parent)
if root_dir not in sys.path:
    sys.path.append(root_dir)

from ai_translator.model.model import Model
from dashscope import Generation
from dashscope.api_entities.dashscope_response import GenerationResponse

class QwenModel(Model):
    def __init__(self, config=None):
        self.api_key = config.get('dashscope_api_key') if config else os.getenv("DASHSCOPE_API_KEY")

    def make_request(self, prompt):
        try:
            response = Generation.call(
                model='qwen-max',
                api_key=self.api_key,
                messages=[{"role": "user", "content": prompt}],
                result_format='message'
            )
            if response.status_code == 200:
                return response.output.choices[0].message.content, True
            else:
                raise Exception(f"API请求失败: {response.message}")
        except Exception as e:
            raise Exception(f"发生未知错误: {e}")

