from .content import Content

# Page
# 用于存储页面内容
class Page:
    # 获取页面内容
    def __init__(self):
        self.contents = []
    
    # 添加页面内容
    def add_content(self, content: Content):
        self.contents.append(content)