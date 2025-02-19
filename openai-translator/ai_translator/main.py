import sys
import os
from typing import Optional

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, ConfigLoader, LOG
from ai_translator.model import GLMModel, OpenAIModel, DeepseekModel, QwenModel, KimiModel
from translator import PDFTranslator

def create_model(model_type: str) -> any:
    """根据类型创建对应的模型实例

    Args:
        model_type: 模型类型，支持 'openai', 'glm', 'deepseek', 'qwen', 'kimi'

    Returns:
        model: 模型实例
    """
    model_type = model_type.lower()
    if model_type == 'openai':
        return OpenAIModel()
    elif model_type == 'glm':
        return GLMModel()
    elif model_type == 'deepseek':
        return DeepseekModel()
    elif model_type == 'qwen':
        return QwenModel()
    elif model_type == 'kimi':
        return KimiModel()
    else:
        raise ValueError(f'不支持的模型类型: {model_type}')

if __name__ == "__main__":
    # 解析命令行参数
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()
    
    # 获取模型类型
    model_type = args.model
    
    try:
        # 创建模型实例
        model = create_model(model_type)
        LOG.info(f'使用模型: {model_type}')

        # 获取输入文件
        pdf_file_path = args.book

        # 实例化 PDFTranslator 并开始翻译
        translator = PDFTranslator(model)
        translator.translate_pdf(pdf_file_path)
        
    except Exception as e:
        LOG.error(f'翻译过程中发生错误: {str(e)}')
        sys.exit(1)
