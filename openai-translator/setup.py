from setuptools import setup, find_packages

setup(
    name="ai_translator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'openai',
        'pdfplumber',
        'simplejson',
        'requests',
        'python-dotenv',
        'pillow',
        'reportlab',
        'pandas',
        'loguru',
        'pathlib',
        'zhipuai',
        'dashscope'
    ],
)
