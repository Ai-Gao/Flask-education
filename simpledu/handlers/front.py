from flask import Blueprint, render_template
from simpledu.models import Course
# 省略　url_prefix(前缀), 默认路径就是'/'

front = Blueprint('front', __name__)

# 路由模块化（Blueprint实现）

@front.route('/')
def index():
# 查询表Course中的数据
    courses = Course.query.all()
    return render_template('index.html', courses=courses)


