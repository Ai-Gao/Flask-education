# coding='utf-8'

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for


# db实例化对象不再传入　app对象
# 创建数据库ORM对象
db = SQLAlchemy()

# 创建基类，方便以后创建的表使用
class Base(db.Model, UserMixin):
    # 继承UserMixin 使用is_authenticated property() 判断用户是否登录状态

    """ 所有model的一个基类，默认添加了时间戳"""
    # 不要把这个表当做 Model类, 即不在数据库中创建该表,可以当做基类
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)




class User(Base):
    __tablename__ = 'user'

# 用数值表示角色，判断用户权限
    ROLE_USER = 10
    ROLE_STAFF = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True,nullable=False)
    _password = db.Column('password',db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    job = db.Column(db.String(64))
    publish_courses = db.relationship('Course')

    # 定义一个__repr__方法，输出调用结果
    def __repr__(self):
        return '<User:{}>'.format(self.username)

    # 属性装饰器，将方法当做属性调用
    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    # 将获取的密码与数据库中的比对
    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_staff(self):
        return self.role == self.ROLE_STAFF

class Course(Base):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128),unique=True, index=True, nullable=False)
    # 课程描述信息
    description = db.Column(db.String(256))
    # 课程图片　url地址
    image_url = db.Column(db.String(256))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    author = db.relationship('User',uselist=False)
   #author = User.query.filter_by(user_id = author_id).one()
    chapters = db.relationship('Chapter')

    def __repr__(self):
        return '<Course:{}>'.format(self.name)

    @property
    def url(self):
        return url_for('course.detail', course_id=self.id)


class Chapter(Base):
    __tablename__ = 'chapter'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    description = db.Column(db.String(256))
    # 课程视频的　url　地址
    vedio_url = db.Column(db.String(256))

    # 视频时长，格式:'30:15i'，'1:15:20'
    vedio_duration = db.Column(db.String(24))
    #关联到课程，并且课程删除级联删除相关章节
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'))
    course = db.relationship('Course', uselist=False)

    def __repr__(self):
        return '<Chapter:{}>'.format(self.name)


