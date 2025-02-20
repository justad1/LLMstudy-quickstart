# AI-Translator

<p align="center">
    <em>基于大语言模型的多功能翻译工具</em>
</p>

## 项目介绍

AI-Translator 是一个强大的 AI 翻译工具，支持将英文 PDF 文档翻译成中文。该工具支持多种主流大语言模型，采用模块化设计，代码结构清晰，易于扩展和维护。

## 特性

### 已实现功能
- [x] 支持多种主流大语言模型(LLMs)
  - OpenAI GPT-4
  - ChatGLM4
  - Deepseek
  - Qwen-plus
  - Kimi (Moonshot AI)
- [x] PDF 文档翻译能力
  - 支持英文 PDF 翻译为中文
  - 保持原文档的基本结构
- [x] 灵活的配置系统
  - 支持 JSON/YAML 配置文件
  - 支持命令行参数配置
- [x] 健壮的异常处理
  - 完善的日志记录系统
  - 翻译超时和错误处理机制
- [x] 模块化架构设计
  - 清晰的代码结构
  - 易于扩展和维护

### 开发计划
- [x] 用户界面优化
  - 实现 Web 界面，提升易用性
  - 支持实时翻译进度显示
- [ ] 功能扩展
  - 支持多个 PDF 文件批处理
  - 提供 RESTful API 接口
  - 支持更多语言翻译方向
- [ ] 性能提升
  - 优化 PDF 布局和格式保留
  - 提升翻译质量
  - 支持自定义训练的翻译模型

## 快速开始

### 1. 环境准备

1. 克隆项目:
```bash
git clone https://github.com/justad1/openai-quickstart.git
cd openai-translator
```

2. 安装依赖:
```bash
pip install -r requirements.txt
```

### 2. 配置

项目使用环境变量来配置各个模型的 API 密钥，支持以下配置方式：

#### 方式一：环境变量配置（推荐）

在项目根目录创建 `.env` 文件：

```bash
# OpenAI API 配置
OPENAI_API_KEY=your-openai-api-key

# ChatGLM API 配置
GLM_API_KEY=your-glm-api-key

# Deepseek API 配置
DEEPSEEK_API_KEY=your-deepseek-api-key

# Qwen API 配置
DASHSCOPE_API_KEY=your-qwen-api-key

# Moonshot (Kimi) API 配置
MOONSHOT_API_KEY=your-moonshot-api-key
```

#### 方式二：命令行参数
1. 首先导入apikey到环境变量
```bash

echo "export OPENAI_API_KEY='YOUR_OPENAI_API_KEY'" >> ~/.bashrc
echo "export CHATGLM_API_KEY='YOUR_CHATGLM_API_KEY'" >> ~/.bashrc
echo "export DEEPSEEK_API_KEY='YOUR_DEEPSEEK_API_KEY'" >> ~/.bashrc
echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.bashrc
echo "export MOONSHOT_API_KEY='YOUR_MOONSHOT_API_KEY'" >> ~/.bashrc

source ~/.bashrc

echo $OPENAI_API_KEY
echo $CHATGLM_API_KEY
echo $DEEPSEEK_API_KEY
echo $DASHSCOPE_API_KEY
echo $MOONSHOT_API_KEY
``` 

2. 使用方法
```bash
# OpenAI 模型
python ai_translator/main.py --model openai --book path/to/your.pdf

# ChatGLM 模型
python ai_translator/main.py --model glm --book path/to/your.pdf

# Deepseek 模型
python ai_translator/main.py --model deepseek --book path/to/your.pdf

# Qwen 模型
python ai_translator/main.py --model qwen --book path/to/your.pdf

# Kimi 模型
python ai_translator/main.py --model kimi --book path/to/your.pdf
```

注意：使用命令行参数时，程序仍会从环境变量中读取相应的 API 密钥。

### 3. 运行


### 3. Web 启动

启动 Web 服务器：
```bash
python run_web.py
```

访问地址：
- 浏览器打开 `http://localhost:6000`
- 即可使用 AI 翻译 Web 界面

注意事项：
- 确保已安装所有依赖
- 需要提前配置 API Key
- Web 界面支持文件上传和翻译

## 项目结构

```
ai_translator/
├── main.py                 # 主程序入口
├── model/                  # 模型实现
│   ├── model.py           # 基础模型接口
│   ├── openai_model.py     # OpenAI模型
│   ├── glm_model.py        # ChatGLM模型
│   ├── deepseek_model.py   # Deepseek模型
│   ├── qwen_model.py       # Qwen模型
│   └── kimi_model.py       # Kimi模型
├── translator/             # 翻译器实现
│   ├── pdf_translator.py   # PDF翻译器
│   └── writer.py          # 输出格式处理
├── book/                   # 文档处理
│   └── book.py            # PDF解析与处理
└── utils/                 # 工具函数
    ├── config_loader.py   # 配置加载
    └── logger.py         # 日志处理
```

## 依赖说明

主要依赖包括:
- openai
- pdfplumber
- python-dotenv
- requests
- loguru
- pillow
- reportlab
- pandas

详细依赖请查看 `requirements.txt`。

## 注意事项

1. API 密钥配置
   - 使用前请确保已在 `.env` 文件中配置正确的 API Key
   - 不同模型需要配置各自的环境变量
   - API Key 不要提交到代码仓库
   
2. PDF 文件要求
   - 确保 PDF 文件是文本可选择的格式
   - 避免使用扫描版 PDF
   
3. 使用建议
   - 翻译大文件时请注意 API 调用次数和费用
   - 建议先用小文件测试配置是否正确
   - 保持网络连接稳定
   - 不同模型的翻译质量和速度可能不同，建议测试后选择最适合的模型

## 许可证

该项目采用 GPL-3.0 许可证。详情请查看 [LICENSE](LICENSE) 文件。
