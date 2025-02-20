from flask import Flask, render_template, request, jsonify, Response, send_from_directory
from flask_cors import CORS
import json
import os
from pathlib import Path
from ..translator.pdf_translator import PDFTranslator
from ..model import get_model_class
from ..config import get_config

app = Flask(__name__)
CORS(app)

# 全局变量存储翻译进度
translation_progress = {"current": 0, "total": 0, "status": "idle"}

def event_stream():
    """用于SSE的事件流生成器"""
    while True:
        # 发送当前进度
        data = json.dumps(translation_progress)
        yield f"data: {data}\n\n"
        if translation_progress["status"] == "completed":
            break

@app.route('/')
def index():
    """渲染主页"""
    return render_template('index.html')

@app.route('/progress')
def progress():
    """SSE端点，用于实时进度更新"""
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/translate', methods=['POST'])
def translate():
    """处理翻译请求"""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "Only PDF files are supported"}), 400

    # 获取项目根目录
    root_dir = Path(__file__).resolve().parents[3]
    
    # 保存上传的文件
    upload_dir = root_dir / "uploads"
    upload_dir.mkdir(exist_ok=True)
    pdf_path = upload_dir / file.filename
    file.save(pdf_path)

    # 获取选择的模型
    model_name = request.form.get('model', 'gpt')  # 默认使用GPT模型
    config = get_config()
    model_class = get_model_class(model_name)
    model = model_class(config)

    # 创建翻译器实例
    translator = PDFTranslator(model)

    # 更新进度状态
    translation_progress["status"] = "translating"
    translation_progress["current"] = 0
    translation_progress["total"] = 100  # 这里需要实际计算总页数

    try:
        # 开始翻译
        output_path = translator.translate_pdf(str(pdf_path))
        
        # 更新完成状态
        translation_progress["status"] = "completed"
        translation_progress["current"] = translation_progress["total"]

        # 获取文件名
        output_filename = os.path.basename(output_path)
        
        return jsonify({
            "success": True,
            "output_filename": output_filename
        })
    except Exception as e:
        translation_progress["status"] = "error"
        return jsonify({"error": str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """处理文件下载请求"""
    # 使用相对路径处理下载
    return send_from_directory('../../../output', filename, as_attachment=True)

def run_web_app():
    """启动Web应用"""
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    run_web_app()
