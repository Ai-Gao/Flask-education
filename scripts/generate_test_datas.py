import os
import json
from random import randint
from faker import Faker
from simpledu.models import db, User, Course, Chapter

# 创建　faker 工厂
fake = Faker()

#　生成一个教师用户
def iter_users():
    yield User(
            username='Jack Lee' ,
            email ='jacklee@example.com',
            password='zxcvbnm',
            job='研发工程师'
            )

# 从datas读取实验楼课程数据，生成测试数据，将课程教师设置为生成的教师用户

def iter_courses():
    author = User.query.filter_by(username='aimme').first()
   # with open(os.path.join(os.path.dirname(__file__), '..', 'datas', 'courses.json')) as f:
   #     courses = json.load(f)
    for course in range(20):
        yield Course(
               name=fake.sentence(),
                description=fake.sentence(),
                image_url='www.baidu.com',
                author=author
                )

def iter_chapters():
    for course in Course.query:
        for i in range(randint(3,10)):
            yield Chapter(
                    name=fake.sentence(),
                    course=course,
                    vedio_url='https://labfile.oss.aliyuncs.com/courses/923/week2_mp4/2-1-1-mac.mp4',
                    vedio_duration='{}:{}'.format(randint(10,30), randint(10,59))
                    )

def run():
    for user in iter_users():
        db.session.add(user)

    for course in iter_courses():
        db.session.add(course)

    for chapter in iter_chapters():
        db.session.add(chapter)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
