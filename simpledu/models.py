from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# db实例化对象不再传入　app对象
# 创建数据库ORM对象
db = SQLAlchemy()

# 创建基类，方便以后创建的表使用
class Base(db.Model):

    """ 所有model的一个基类，默认添加了时间戳"""
    # 不要把这个表当做 Model类, 即不在数据库中创建该表,可以当做基类
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)




class User(Base):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    publish_courses = db.relationship('Course')

class Course(Base):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128),unique=True, index=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    author = db.relationship('User',uselist=False)

