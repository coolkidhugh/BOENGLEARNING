import csv
import os
import random
from src.models.user import db
from src.models.word import Word
from flask import Flask

# 创建一个临时的Flask应用上下文
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///english_learning.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 预设单词数据
preset_words = [
    {"english": "apple", "chinese": "苹果", "category": "food", "image_path": "/static/images/food/apple.jpg"},
    {"english": "banana", "chinese": "香蕉", "category": "food", "image_path": "/static/images/food/banana.jpg"},
    {"english": "orange", "chinese": "橙子", "category": "food", "image_path": "/static/images/food/orange.jpg"},
    {"english": "dog", "chinese": "狗", "category": "animals", "image_path": "/static/images/animals/dog.jpg"},
    {"english": "cat", "chinese": "猫", "category": "animals", "image_path": "/static/images/animals/cat.jpg"},
    {"english": "bird", "chinese": "鸟", "category": "animals", "image_path": "/static/images/animals/bird.jpg"},
    {"english": "car", "chinese": "汽车", "category": "transport", "image_path": "/static/images/transport/car.jpg"},
    {"english": "bus", "chinese": "公交车", "category": "transport", "image_path": "/static/images/transport/bus.jpg"},
    {"english": "train", "chinese": "火车", "category": "transport", "image_path": "/static/images/transport/train.jpg"},
    {"english": "book", "chinese": "书", "category": "daily", "image_path": "/static/images/daily/book.jpg"},
    {"english": "pen", "chinese": "钢笔", "category": "daily", "image_path": "/static/images/daily/pen.jpg"},
    {"english": "phone", "chinese": "手机", "category": "daily", "image_path": "/static/images/daily/phone.jpg"},
    {"english": "sun", "chinese": "太阳", "category": "nature", "image_path": "/static/images/nature/sun.jpg"},
    {"english": "moon", "chinese": "月亮", "category": "nature", "image_path": "/static/images/nature/moon.jpg"},
    {"english": "star", "chinese": "星星", "category": "nature", "image_path": "/static/images/nature/star.jpg"},
    {"english": "water", "chinese": "水", "category": "nature", "image_path": "/static/images/nature/water.jpg"},
    {"english": "bread", "chinese": "面包", "category": "food", "image_path": "/static/images/food/bread.jpg"},
    {"english": "milk", "chinese": "牛奶", "category": "food", "image_path": "/static/images/food/milk.jpg"},
    {"english": "coffee", "chinese": "咖啡", "category": "food", "image_path": "/static/images/food/coffee.jpg"},
    {"english": "tea", "chinese": "茶", "category": "food", "image_path": "/static/images/food/tea.jpg"},
    {"english": "elephant", "chinese": "大象", "category": "animals", "image_path": "/static/images/animals/elephant.jpg"},
    {"english": "lion", "chinese": "狮子", "category": "animals", "image_path": "/static/images/animals/lion.jpg"},
    {"english": "tiger", "chinese": "老虎", "category": "animals", "image_path": "/static/images/animals/tiger.jpg"},
    {"english": "monkey", "chinese": "猴子", "category": "animals", "image_path": "/static/images/animals/monkey.jpg"},
    {"english": "bicycle", "chinese": "自行车", "category": "transport", "image_path": "/static/images/transport/bicycle.jpg"},
    {"english": "airplane", "chinese": "飞机", "category": "transport", "image_path": "/static/images/transport/airplane.jpg"},
    {"english": "ship", "chinese": "船", "category": "transport", "image_path": "/static/images/transport/ship.jpg"},
    {"english": "motorcycle", "chinese": "摩托车", "category": "transport", "image_path": "/static/images/transport/motorcycle.jpg"},
    {"english": "table", "chinese": "桌子", "category": "daily", "image_path": "/static/images/daily/table.jpg"},
    {"english": "chair", "chinese": "椅子", "category": "daily", "image_path": "/static/images/daily/chair.jpg"},
    {"english": "bed", "chinese": "床", "category": "daily", "image_path": "/static/images/daily/bed.jpg"},
    {"english": "door", "chinese": "门", "category": "daily", "image_path": "/static/images/daily/door.jpg"},
    {"english": "window", "chinese": "窗户", "category": "daily", "image_path": "/static/images/daily/window.jpg"},
    {"english": "computer", "chinese": "电脑", "category": "daily", "image_path": "/static/images/daily/computer.jpg"},
    {"english": "television", "chinese": "电视", "category": "daily", "image_path": "/static/images/daily/television.jpg"},
    {"english": "river", "chinese": "河流", "category": "nature", "image_path": "/static/images/nature/river.jpg"},
    {"english": "mountain", "chinese": "山", "category": "nature", "image_path": "/static/images/nature/mountain.jpg"},
    {"english": "forest", "chinese": "森林", "category": "nature", "image_path": "/static/images/nature/forest.jpg"},
    {"english": "ocean", "chinese": "海洋", "category": "nature", "image_path": "/static/images/nature/ocean.jpg"},
    {"english": "flower", "chinese": "花", "category": "nature", "image_path": "/static/images/nature/flower.jpg"},
    {"english": "tree", "chinese": "树", "category": "nature", "image_path": "/static/images/nature/tree.jpg"},
    {"english": "grass", "chinese": "草", "category": "nature", "image_path": "/static/images/nature/grass.jpg"},
    {"english": "sky", "chinese": "天空", "category": "nature", "image_path": "/static/images/nature/sky.jpg"},
    {"english": "cloud", "chinese": "云", "category": "nature", "image_path": "/static/images/nature/cloud.jpg"},
    {"english": "rain", "chinese": "雨", "category": "nature", "image_path": "/static/images/nature/rain.jpg"},
    {"english": "snow", "chinese": "雪", "category": "nature", "image_path": "/static/images/nature/snow.jpg"},
    {"english": "wind", "chinese": "风", "category": "nature", "image_path": "/static/images/nature/wind.jpg"},
    {"english": "fire", "chinese": "火", "category": "nature", "image_path": "/static/images/nature/fire.jpg"},
    {"english": "earth", "chinese": "地球", "category": "nature", "image_path": "/static/images/nature/earth.jpg"}
]

def seed_data():
    with app.app_context():
        # 检查是否已有预设单词
        existing_count = Word.query.filter_by(is_preset=True).count()
        if existing_count > 0:
            print(f"已存在 {existing_count} 个预设单词，跳过导入")
            return
        
        print("开始导入预设单词...")
        
        # 导入预设单词
        for word_data in preset_words:
            word = Word(
                english=word_data["english"],
                chinese=word_data["chinese"],
                image_path=word_data["image_path"],
                category=word_data["category"],
                is_preset=True
            )
            db.session.add(word)
        
        db.session.commit()
        print(f"成功导入 {len(preset_words)} 个预设单词")

if __name__ == "__main__":
    seed_data()
