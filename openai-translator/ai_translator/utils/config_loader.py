import yaml

class ConfigLoader:
    # 初始化ConfigLoader类，接收配置文件路径作为参数
    def __init__(self, config_path):
        # 配置文件路径
        self.config_path = config_path

    # 加载配置文件并返回配置字典
    def load_config(self):
        # 打开配置文件并读取内容
        with open(self.config_path, "r") as f:
            # 使用yaml库解析配置文件内容，返回配置字典
            config = yaml.safe_load(f)
        return config