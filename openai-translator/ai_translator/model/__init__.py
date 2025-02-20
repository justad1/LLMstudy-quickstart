from .model import Model
from .glm_model import GLMModel
from .openai_model import OpenAIModel
from .deepseek_model import DeepseekModel
from .qwen_model import QwenModel
from .kimi_model import KimiModel

def get_model_class(model_name: str):
    """根据模型名称返回对应的模型类
    
    Args:
        model_name: 模型名称，可选值：'gpt', 'glm', 'deepseek', 'qwen', 'kimi'
        
    Returns:
        对应的模型类
    """
    model_map = {
        'gpt': OpenAIModel,
        'glm': GLMModel,
        'deepseek': DeepseekModel,
        'qwen': QwenModel,
        'kimi': KimiModel
    }
    
    if model_name not in model_map:
        raise ValueError(f'不支持的模型: {model_name}。支持的模型有: {list(model_map.keys())}')
    
    return model_map[model_name]