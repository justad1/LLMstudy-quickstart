from loguru import logger
import os
import sys

# 定义日志文件名和日志轮转时间
LOG_FILE = "translation.log"
ROTATION_TIME = "02:00"

class Logger:
    def __init__(self, name="translation", log_dir="logs", debug=False):
        # 如果日志目录不存在，则创建目录
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file_path = os.path.join(log_dir, LOG_FILE)

        # 移除默认的loguru处理器
        logger.remove()

        # 添加控制台处理器，并根据debug参数设置日志级别
        level = "DEBUG" if debug else "INFO"
        logger.add(sys.stdout, level=level)
        # 添加文件处理器，设置日志轮转时间和日志级别
        logger.add(log_file_path, rotation=ROTATION_TIME, level="DEBUG")
        self.logger = logger

# 创建Logger实例并暴露logger对象
LOG = Logger(debug=True).logger

if __name__ == "__main__":
    # 测试日志功能
    log = Logger().logger

    log.debug("This is a debug message.")
    log.info("This is an info message.")
    log.warning("This is a warning message.")
    log.error("This is an error message.")