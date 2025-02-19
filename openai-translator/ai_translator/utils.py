import argparse
import json
import logging
import os
from typing import Dict, Any

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
LOG = logging.getLogger('AI-Translator')

class ArgumentParser:
    """命令行参数解析器"""
    
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='AI Translator - 多模型支持的 PDF 翻译工具')
        self._add_arguments()

    def _add_arguments(self):
        """添加命令行参数"""
        self.parser.add_argument(
            '--model',
            type=str,
            help='选择要使用的模型 (openai/glm/deepseek/qwen)',
            default='openai'
        )
        self.parser.add_argument(
            '--book',
            type=str,
            help='PDF 文件路径'
        )
        self.parser.add_argument(
            '--file_format',
            type=str,
            choices=['PDF', 'Markdown'],
            help='输出文件格式 (PDF/Markdown)',
            default='PDF'
        )
        self.parser.add_argument(
            '--config',
            type=str,
            help='配置文件路径',
            default='config.json'
        )
        # OpenAI 特定参数
        self.parser.add_argument(
            '--openai_model',
            type=str,
            help='OpenAI 模型名称'
        )
        self.parser.add_argument(
            '--openai_api_key',
            type=str,
            help='OpenAI API 密钥'
        )

    def parse_arguments(self) -> argparse.Namespace:
        """解析命令行参数

        Returns:
            解析后的参数对象
        """
        return self.parser.parse_args()

class ConfigLoader:
    """配置文件加载器"""
    
    def __init__(self, config_path: str):
        """
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path

    def load_config(self) -> Dict[str, Any]:
        """加载配置文件

        Returns:
            配置字典

        Raises:
            FileNotFoundError: 配置文件不存在
            json.JSONDecodeError: 配置文件格式错误
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f'配置文件不存在: {self.config_path}')

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f'配置文件格式错误: {str(e)}', e.doc, e.pos)
