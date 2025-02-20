import os
from typing import Optional
from tqdm import tqdm
from ai_translator.model import Model
from ai_translator.translator.pdf_parser import PDFParser
from ai_translator.translator.writer import Writer
from ai_translator.utils import LOG
from ai_translator.book import Book, Page, Content, ContentType, TableContent

class PDFTranslator:
    """
    PDF翻译器类，负责将PDF文件内容翻译成目标语言并保存翻译结果。
    """
    def __init__(self, model: Model):
        """
        初始化PDF翻译器。

        Args:
            model (Model): 用于翻译的模型。
        """
        self.model = model
        self.pdf_parser = PDFParser()
        self.writer = Writer()

    def translate_pdf(self, pdf_file_path: str, target_language: str = '中文', pages: Optional[int] = None):
        """
        翻译指定的PDF文件并保存翻译结果。

        Args:
            pdf_file_path (str): PDF文件的路径。
            file_format (str, optional): 输出文件的格式，默认为'PDF'。
            target_language (str, optional): 目标语言，默认为'中文'。
            output_file_path (str, optional): 输出文件的路径，如果为None则不保存。
            pages (Optional[int], optional): 要翻译的页数，如果为None则翻译所有页面。
        """
        # 解析PDF文件
        self.book = self.pdf_parser.parse_pdf(pdf_file_path, pages)

        # 初始化进度条
        total_contents = sum(len(page.contents) for page in self.book.pages)
        progress_bar = tqdm(total=total_contents, desc='翻译进度', unit='项')

        # 逐页翻译PDF内容
        for page_idx, page in enumerate(self.book.pages):
            for content_idx, content in enumerate(page.contents):
                # 生成翻译提示
                prompt = self.model.translate_prompt(content, target_language)
                LOG.debug(prompt)
                
                # 请求翻译
                translation, status = self.model.make_request(prompt)
                LOG.info(translation)
                
                # 更新翻译结果到Book对象中
                self.book.pages[page_idx].contents[content_idx].set_translation(translation, status)
                
                # 更新进度条
                progress_bar.update(1)
        
        # 关闭进度条
        progress_bar.close()

        # 生成输出文件路径
        filename = os.path.basename(pdf_file_path)
        output_filename = os.path.splitext(filename)[0] + '_translated.pdf'
        output_path = os.path.join('output', output_filename)
        
        # 创建输出目录
        os.makedirs('output', exist_ok=True)
        
        # 保存翻译后的内容
        self.writer.save_translated_book(self.book, output_path, 'pdf')
        LOG.info(f"翻译后的文件已保存到: {output_path}")
        
        # 返回输出文件路径
        return output_path