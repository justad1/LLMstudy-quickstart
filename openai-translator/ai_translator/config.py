import os
from pathlib import Path
from dotenv import load_dotenv

def get_config():
    """获取配置信息
    
    Returns:
        包含配置信息的字典
    """
    # 加载环境变量
    load_dotenv()
    
    # 基础配置
    config = {
        # API Keys
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'glm_api_key': os.getenv('GLM_API_KEY'),
        'deepseek_api_key': os.getenv('DEEPSEEK_API_KEY'),
        'dashscope_api_key': os.getenv('DASHSCOPE_API_KEY'),
        'moonshot_api_key': os.getenv('MOONSHOT_API_KEY'),
        
        # 文件路径配置
        'upload_dir': str(Path('uploads').absolute()),
        'output_dir': str(Path('output').absolute()),
        
        # Web应用配置
        'host': '0.0.0.0',
        'port': 5000,
        'debug': True
    }
    
    # 创建必要的目录
    Path(config['upload_dir']).mkdir(exist_ok=True)
    Path(config['output_dir']).mkdir(exist_ok=True)
    
    return config
