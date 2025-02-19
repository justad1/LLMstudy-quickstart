import pdfplumber
from typing import Optional
from ai_translator.book import Book, Page, Content, ContentType, TableContent
from ai_translator.translator.exceptions import PageOutOfRangeException
from ai_translator.utils import LOG


class PDFParser:
    """
    PDF解析器类，用于解析PDF文件并提取文本和表格内容。
    """
    def __init__(self):
        """
        初始化PDF解析器。
        """
        pass

    def parse_pdf(self, pdf_file_path: str, pages: Optional[int] = None) -> Book:
        """
        解析指定的PDF文件并返回一个Book对象。

        Args:
            pdf_file_path (str): PDF文件的路径。
            pages (Optional[int]): 要解析的页数，如果为None则解析所有页面。

        Returns:
            Book: 包含解析结果的Book对象。

        Raises:
            PageOutOfRangeException: 如果指定的页数超过了PDF的实际页数。
        """
        book = Book(pdf_file_path)

        with pdfplumber.open(pdf_file_path) as pdf:
            # 检查指定的页数是否超出PDF的实际页数
            if pages is not None and pages > len(pdf.pages):
                raise PageOutOfRangeException(len(pdf.pages), pages)
            
            # 确定要解析的页面范围
            if pages is None:
                pages_to_parse = pdf.pages
            else:
                pages_to_parse = pdf.pages[:pages]
                
            # 逐页解析PDF内容
            for pdf_page in pages_to_parse:
                page = Page()
                
                # 提取原始文本内容
                raw_text = pdf_page.extract_text()
                tables = pdf_page.extract_tables()
                
                # 处理文本内容
                if raw_text:
                    # 移除空行和前后空白字符
                    raw_text_lines = raw_text.splitlines()
                    cleaned_raw_text_lines = [line.strip() for line in raw_text_lines if line.strip()]
                    cleaned_raw_text = "\n".join(cleaned_raw_text_lines)
                    
                    # 创建文本内容对象并添加到页面中
                    text_content = Content(content_type=ContentType.TEXT, original=cleaned_raw_text)
                    page.add_content(text_content)
                    LOG.debug(f"[raw_text]\n {cleaned_raw_text}")

                # 处理表格内容
                if tables:
                    for table_data in tables:
                        if table_data:
                            table = TableContent(table_data)
                            page.add_content(table)
                            LOG.debug(f"[table]\n{table}")

                # 将解析后的页面添加到Book对象中
                book.add_page(page)

        return book