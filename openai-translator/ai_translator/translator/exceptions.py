class PageOutOfRangeException(Exception):
    """异常类，用于处理请求的页面超出书籍总页数的情况。"""
    def __init__(self, book_pages, requested_pages):
        """
        初始化异常实例。
        
        :param book_pages: 书籍的总页数。
        :param requested_pages: 请求的页数。
        """
        self.book_pages = book_pages
        self.requested_pages = requested_pages
        super().__init__(f"Page out of range: Book has {book_pages} pages, but {requested_pages} pages were requested.")