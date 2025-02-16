import argparse

# 定义ArgumentParser类，用于解析命令行参数
class ArgumentParser:
    def __init__(self):
        # 初始化 ArgumentParser 对象，用于解析命令行参数
        self.parser = argparse.ArgumentParser(description='Translate English PDF book to Chinese.')
        
        # 添加配置文件的参数
        self.parser.add_argument('--config', type=str, default='config.yaml', help='Configuration file with model and API settings.')
        
        # 添加模型类型的参数，必需且只能从指定选项中选择
        self.parser.add_argument('--model_type', type=str, required=True, choices=['chatglm','openai','qwen','kimi','deepseek'], help='The type of translation model to use. Choose "chatglmModel","openaiModel","qwenModel","kimiModel","deepseekModel".')
        
        # 添加 API 请求超时时间的参数
        self.parser.add_argument('--timeout', type=int, help='Timeout for the API request in seconds.')
        
        # 添加 OpenAI 模型名称的参数
        self.parser.add_argument('--openai_model', type=str, help='The model name of OpenAI Model. Required if model_type is "OpenAIModel".')
        self.parser.add_argument('--openai_api_key', type=str, help='The API key for OpenAIModel. Required if model_type is "OpenAIModel".')
        
        # 添加 ChatGLM 模型名称的参数
        self.parser.add_argument('--chatglm_model', type=str, help='The model name of chatglm Model. Required if model_type is "chatglmModel".')
        self.parser.add_argument('--chatglm_api_key', type=str, help='The API key for chatglmModel. Required if model_type is "chatglmModel".')
        
        # 添加 Qwen 模型名称的参数
        self.parser.add_argument('--qwen_model', type=str, help='The model name of qwen Model. Required if model_type is "qwenModel".')
        self.parser.add_argument('--qwen_api_key', type=str, help='The API key for qwenModel. Required if model_type is "qwenModel".')
        
        # 添加 Kimi 模型名称的参数
        self.parser.add_argument('--kimi_model', type=str, help='The model name of kimi Model. Required if model_type is "kimiModel".')
        self.parser.add_argument('--kimi_api_key', type=str, help='The API key for kimiModel. Required if model_type is "kimiModel".')
        
        # 添加 Deepseek 模型名称的参数
        self.parser.add_argument('--deepseek_model', type=str, help='The model name of deepseek Model. Required if model_type is "deepseekModel".')
        self.parser.add_argument('--deepseek_api_key', type=str, help='The API key for deepseekModel. Required if model_type is "deepseekModel".')
        
        # 添加要翻译的 PDF 书籍文件的参数
        self.parser.add_argument('--book', type=str, help='PDF file to translate.')
        
        # 添加翻译后书籍文件格式的参数
        self.parser.add_argument('--file_format', type=str, help='The file format of translated book. Now supporting PDF and Markdown')   
        
    def parse_arguments(self):
        # 解析命令行参数
        args = self.parser.parse_args()  # 使用正确的解析器对象
        
        # 检查 OpenAI 模型所需的参数是否提供
        if args.model_type == 'OpenAIModel' and not args.openai_model and not args.openai_api_key:
            self.parser.error("--openai_model and --openai_api_key is required when using OpenAIModel")
            return args
        
        # 检查 ChatGLM 模型所需的参数是否提供
        if args.model_type == 'chatglmModel' and not args.chatglm_model and not args.chatglm_api_key:
            self.parser.error("--chatglm_model and --chatglm_api_key is required when using chatglmModel")
            return args
        
        # 检查 Qwen 模型所需的参数是否提供
        if args.model_type == 'qwenModel' and not args.qwen_model and not args.qwen_api_key:
            self.parser.error("--qwen_model and --qwen_api_key is required when using qwenModel")
            return args
        
        # 检查 Kimi 模型所需的参数是否提供
        if args.model_type == 'kimiModel' and not args.kimi_model and not args.kimi_api_key:
            self.parser.error("--kimi_model and --kimi_api_key is required when using kimiModel")
            return args
        
        # 检查 Deepseek 模型所需的参数是否提供
        if args.model_type == 'deepseekModel' and not args.deepseek_model and not args.deepseek_api_key:
            self.parser.error("--deepseek_model and --deepseek_api_key is required when using deepseekModel")
            return args