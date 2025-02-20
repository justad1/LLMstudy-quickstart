# 导入必要的模块和库
import os
from reportlab.lib import colors, pagesizes, units  # PDF 样式和布局相关库
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  # 文本样式
from reportlab.pdfbase import pdfmetrics  # PDF 字体注册
from reportlab.pdfbase.ttfonts import TTFont  # TrueType 字体支持
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)  # PDF 文档创建和元素

# 导入自定义模块
from ai_translator.book import Book, ContentType  # 书籍和内容类型
from ai_translator.utils import LOG  # 日志记录

class Writer:
    """
    书籍写入器类，负责将翻译后的书籍保存为不同格式的文件
    支持 PDF 和 Markdown 两种输出格式
    """
    def __init__(self):
        """
        初始化方法，目前没有特殊的初始化逻辑
        """
        pass

    def save_translated_book(self, book: Book, output_file_path: str = None, file_format: str = "PDF"):
        """
        根据指定的文件格式保存翻译后的书籍
        
        参数:
        - book: 翻译后的书籍对象
        - output_file_path: 输出文件路径，默认为 None（自动生成）
        - file_format: 输出文件格式，支持 "PDF" 和 "Markdown"
        
        异常:
        - 如果文件格式不支持，抛出 ValueError
        """
        if file_format.lower() == "pdf":
            self._save_translated_book_pdf(book, output_file_path)
        elif file_format.lower() == "markdown":
            self._save_translated_book_markdown(book, output_file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_format}")

    def _save_translated_book_pdf(self, book: Book, output_file_path: str = None):
        """
        将翻译后的书籍保存为 PDF 文件
        
        参数:
        - book: 翻译后的书籍对象
        - output_file_path: PDF 输出文件路径，默认为 None（自动生成）
        """
        # 如果未指定输出路径，自动生成基于原 PDF 文件的新文件名
        if output_file_path is None:
            output_file_path = book.pdf_file_path.replace('.pdf', f'_translated.pdf')

        LOG.info(f"pdf_file_path: {book.pdf_file_path}")
        LOG.info(f"开始翻译: {output_file_path}")

        # 注册中文字体（宋体）
        font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'fonts', 'simsun.ttc')
        pdfmetrics.registerFont(TTFont("SimSun", font_path))

        # 创建自定义段落样式，使用宋体
        title_style = ParagraphStyle(
            'Title',
            fontName='SimSun',
            fontSize=16,
            leading=20,
            alignment=1,  # 居中对齐
            spaceAfter=30,
            textColor=colors.HexColor('#2C3E50')
        )
        heading_style = ParagraphStyle(
            'Heading',
            fontName='SimSun',
            fontSize=14,
            leading=18,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.HexColor('#34495E')
        )
        text_style = ParagraphStyle(
            'Text',
            fontName='SimSun',
            fontSize=12,
            leading=16,
            spaceBefore=6,
            spaceAfter=6,
            textColor=colors.HexColor('#2C3E50')
        )

        # 创建 PDF 文档
        doc = SimpleDocTemplate(output_file_path, pagesize=pagesizes.letter)
        styles = getSampleStyleSheet()
        story = []  # 存储 PDF 内容的列表

        # 遍历书籍的每一页和内容
        for page in book.pages:
            for content in page.contents:
                if content.status:  # 如果内容已翻译
                    if content.content_type == ContentType.TEXT:
                        # 添加翻译后的文本段落
                        text = content.translation
                        # 检查是否是标题或小标题
                        if text.strip().startswith('#'):
                            if text.strip().startswith('##'):
                                para = Paragraph(text.replace('##', '').strip(), heading_style)
                            else:
                                para = Paragraph(text.replace('#', '').strip(), title_style)
                        else:
                            para = Paragraph(text, text_style)
                        story.append(para)

                    elif content.content_type == ContentType.TABLE:
                        # 添加翻译后的表格
                        table = content.translation
                        table_style = TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),  # 表头背景色
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # 表头文字颜色
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 单元格文字居中
                            ('FONTNAME', (0, 0), (-1, 0), 'SimSun'),  # 表头字体
                            ('FONTSIZE', (0, 0), (-1, 0), 14),  # 表头字体大小
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # 表头底部填充
                            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8F9F9')),  # 表格内容背景色
                            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2C3E50')),  # 表格内容文字颜色
                            ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),  # 表格内容字体
                            ('FONTSIZE', (0, 1), (-1, -1), 12),  # 表格内容字体大小
                            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),  # 表格网格线
                            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8F9F9'), colors.HexColor('#FFFFFF')]),  # 交替行背景色
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 所有单元格居中
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 所有单元格垂直居中
                            ('PADDING', (0, 0), (-1, -1), 6),  # 所有单元格的内边距
                        ])
                        pdf_table = Table(table.values.tolist())
                        pdf_table.setStyle(table_style)
                        story.append(pdf_table)
            
            # 在每页之间添加分页符（最后一页除外）
            if page != book.pages[-1]:
                story.append(PageBreak())

        # 构建并保存 PDF 文件
        doc.build(story)
        LOG.info(f"翻译完成: {output_file_path}")

    def _save_translated_book_markdown(self, book: Book, output_file_path: str = None):
        """
        将翻译后的书籍保存为 Markdown 文件
        
        参数:
        - book: 翻译后的书籍对象
        - output_file_path: Markdown 输出文件路径，默认为 None（自动生成）
        """
        # 如果未指定输出路径，自动生成基于原 PDF 文件的新文件名
        if output_file_path is None:
            output_file_path = book.pdf_file_path.replace('.pdf', f'_translated.md')

        LOG.info(f"pdf_file_path: {book.pdf_file_path}")
        LOG.info(f"开始翻译: {output_file_path}")
        
        # 打开 Markdown 文件进行写入
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            # 遍历书籍的每一页和内容
            for page in book.pages:
                for content in page.contents:
                    if content.status:  # 如果内容已翻译
                        if content.content_type == ContentType.TEXT:
                            # 添加翻译后的文本段落
                            text = content.translation
                            output_file.write(text + '\n\n')

                        elif content.content_type == ContentType.TABLE:
                            # 添加翻译后的表格（Markdown 格式）
                            table = content.translation
                            # 创建表头
                            header = '| ' + ' | '.join(str(column) for column in table.columns) + ' |' + '\n'
                            # 创建分隔线
                            separator = '| ' + ' | '.join(['---'] * len(table.columns)) + ' |' + '\n'
                            # 创建表格内容
                            body = '\n'.join(['| ' + ' | '.join(str(cell) for cell in row) + ' |' for row in table.values.tolist()]) + '\n\n'
                            
                            # 写入 Markdown 表格
                            output_file.write(header + separator + body)

                # 在每页之间添加分隔线（最后一页除外）
                if page != book.pages[-1]:
                    output_file.write('---\n\n')

        LOG.info(f"翻译完成: {output_file_path}")