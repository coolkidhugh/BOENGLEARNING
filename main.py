import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db, User
from src.models.word import Word, UserWord, QuizResult
from src.routes.user import user_bp
from src.routes.word import word_bp
from src.routes.quiz import quiz_bp

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 配置数据库 - 使用SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///english_learning.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db.init_app(app)

# 注册蓝图
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(word_bp, url_prefix='/api/word')
app.register_blueprint(quiz_bp, url_prefix='/api/quiz')

# 静态文件路由
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

# 创建数据库表
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
