from flask import Blueprint, render_template
from simpledu.models import Course
from simpledu.forms import LoginForm, RegisterForm
from flask import flash

# 省略　url_prefix(前缀), 默认路径就是'/'

front = Blueprint('front', __name__)

# 路由模块化（Blueprint实现）

@front.route('/')
def index():
# 查询表Course中的数据
    courses = Course.query.all()
    return render_template('index.html', courses=courses)

@front.route('/login')
def login():
    # 引入LoginForm()表单
    form = LoginForm()
    return render_template('login.html', form=form)

@front.route('/register')
def register():
    # 引入RegisterForm()表单
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录！','sucess')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)
