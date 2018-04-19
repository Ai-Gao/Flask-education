# coding:'utf-8'
from flask import Flask, render_template
from simpledu.config import configs
from simpledu.models import db, Course

"""app.py 用来创建工厂函数，专门用来创建app实力对象 """

def create_app(config):
# 可以根据传入的config名称,加载不同的配置

#实例化一个Flask类对象
    app = Flask(__name__)

# 配置app对象

    app.config.from_object(configs.get(config))

# SQLAlchemy的初始化方式改为使用　init_app

# 将配置好的app传给SQLAlchemy　去动态创建与数据库的映射 """

    db.init_app(app)


    register_blueprints(app)

    return app

# 定义一个用于注册蓝图的函数

def register_blueprints(app):
    from .handlers import front, course, admin
    app.register_blueprint(front)
    app.register_blueprint(course)
    app.register_blueprint(admin)


