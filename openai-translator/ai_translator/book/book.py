from ai_translator.book.page import Page


# Book类
# 用于存储PDF文件的内容
class Book:
    # 获取PDF文件的内容，将页面的内容存储在pages列表中
    def __init__(self,pdf_file_path):
        self.pdf_file_path = pdf_file_path
        self.pages = []
        
    # 将页面的内容添加到pages列表中 
    def add_page(self,page:Page):
        self.pages.append(page)
        