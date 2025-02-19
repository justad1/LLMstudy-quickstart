# 导入所需模块
import pandas as pd
from enum import Enum, auto
from PIL import Image as PILImage
from ai_translator.utils import LOG

# 定义内容类型枚举
class ContentType(Enum):
    TEXT = auto()   # 文本段落
    TABLE = auto()  # 表格数据
    IMAGE = auto()  # 图片元素

# 定义基础内容类
class Content:
    def __init__(self, content_type, original, translation=None):
        # 初始化内容类型、原文、翻译和状态
        self.content_type = content_type
        self.original = original
        self.translation = translation
        self.status = False

    def set_translation(self, translation, status):
        # 设置翻译内容并验证类型
        if not self.check_translation_type(translation):
            raise ValueError(f"Invalid translation type. Expected {self.content_type}, but got {type(translation)}")
        self.translation = translation
        self.status = status

    def check_translation_type(self, translation):
        # 检查翻译内容的类型是否匹配
        if self.content_type == ContentType.TEXT and isinstance(translation, str):
            return True
        elif self.content_type == ContentType.TABLE and isinstance(translation, list):
            return True
        elif self.content_type == ContentType.IMAGE and isinstance(translation, PILImage.Image):
            return True
        return False

# 定义表格内容类，继承自Content类
class TableContent(Content):
    def __init__(self, data, translation=None):
        # 将数据转换为DataFrame对象
        df = pd.DataFrame(data)

        # 验证数据行数和列数是否匹配
        if len(data) != len(df) or len(data[0]) != len(df.columns):
            raise ValueError("The number of rows and columns in the extracted table data and DataFrame object do not match.")
        
        # 调用父类初始化方法
        super().__init__(ContentType.TABLE, df)

    def set_translation(self, translation, status):
        try:
            # 设置翻译内容并处理成DataFrame格式
            if not isinstance(translation, str):
                raise ValueError(f"Invalid translation type. Expected str, but got {type(translation)}")

            LOG.debug(translation)
            # 将字符串转换为列表的列表
            table_data = [row.strip().split() for row in translation.strip().split('\n')]
            LOG.debug(table_data)
            # 从table_data创建DataFrame
            translated_df = pd.DataFrame(table_data[1:], columns=table_data[0])
            LOG.debug(translated_df)
            self.translation = translated_df
            self.status = status
        except Exception as e:
            # 处理翻译过程中的错误
            LOG.error(f"An error occurred during table translation: {e}")
            self.translation = None
            self.status = False

    def __str__(self):
        # 返回原始内容的字符串表示
        return self.original.to_string(header=False, index=False)

    def iter_items(self, translated=False):
        # 迭代表格中的每个项
        target_df = self.translation if translated else self.original
        for row_idx, row in target_df.iterrows():
            for col_idx, item in enumerate(row):
                yield (row_idx, col_idx, item)

    def update_item(self, row_idx, col_idx, new_value, translated=False):
        # 更新表格中的某个项
        target_df = self.translation if translated else self.original
        target_df.at[row_idx, col_idx] = new_value

    def get_original_as_str(self):
        # 获取原始内容的字符串表示
        return self.original.to_string(header=False, index=False)