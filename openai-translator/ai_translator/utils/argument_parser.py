import argparse

class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Translate English PDF book to Chinese.')
        
        # 添加模型类型的参数
        self.parser.add_argument('--model', type=str, required=True, 
                                choices=['openai', 'glm', 'qwen', 'kimi', 'deepseek'],
                                help='The type of translation model to use')
        
        # 添加输入文件的参数
        self.parser.add_argument('--book', type=str, required=True,
                                help='Path to the input PDF file')

    def parse_arguments(self):
        return self.parser.parse_args()
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