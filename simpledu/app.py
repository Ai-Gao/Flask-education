# coding:'utf-8'
from flask import Flask, render_template
from simpledu.config import configs
from simpledu.models import db, Course, User
from flask_migrate import Migrate
from flask_login import LoginManager

"""app.py 用来创建工厂函数，专门用来创建app实力对象 """

def create_app(config):
# 可以根据传入的config名称,加载不同的配置

#实例化一个Flask类对象
    app = Flask(__name__)

# 配置app对象

    app.config.from_object(configs.get(config))

# SQLAlchemy的初始化方式改为使用　init_app

# 将配置好的app传给SQLAlchemy　去动态创建与数据库的映射 """

    #db.init_app(app)

    #Migrate(app, db)

    # 注册拓展 flask_login
    register_extensions(app)
    register_blueprints(app)

    return app

# 定义一个用于注册蓝图的函数

def register_blueprints(app):
    from .handlers import front, course, admin
    app.register_blueprint(front)
    app.register_blueprint(course)
    app.register_blueprint(admin)

# 定义register_extensions函数，用于将Flask拓展注册到app

def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)
# 从Flask_login导入LoginManager(登录管理器)后，创建该类的实例对象
    login_manager = LoginManager()
    login_manager.init_app(app)
# 使用user_loader装饰器注册一个函数，用来告诉flask_login如何加载用户对象
    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view = 'front.login'
