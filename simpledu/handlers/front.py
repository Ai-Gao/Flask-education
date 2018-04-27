from flask import Blueprint, render_template, redirect, url_for,request, current_app
from simpledu.models import User, Course
from simpledu.forms import LoginForm, RegisterForm
from flask import flash
from flask_login import login_user, logout_user, login_required

# 省略　url_prefix(前缀), 默认路径就是'/'

front = Blueprint('front', __name__)

# 路由模块化（Blueprint实现）

@front.route('/')
def index():
    # 获取参数中传过来的页数
    page = request.args.get('page', default=1, type=int)

    # 生成分页对象
    pagination = Course.query.paginate(
           page=page,
           per_page=current_app.config['INDEX_PER_PAGE'],
           error_out=False
        )
    return render_template('index.html', pagination=pagination)


"""
    # 查询表Course中的数据
    courses = Course.query.all()
    return render_template('index.html', courses=courses)
"""

@front.route('/login', methods=['GET', 'POST'])
def login():
    # 引入LoginForm()表单
# user = User.query.filter_by(email=form.email.data).first()
    form = LoginForm()
    if form.validate_on_submit():
        username = User.query.filter_by(username=form.username.data).first()
        login_user(username, form.remember_me.data)
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)

# 实现登出功能　在用户登录状态下，调用logout_user()
@front.route('/logout')
@login_required
# 使用login_required装饰视图，将确保当前用户调用实际视图前登录并进行验证
def logout():
    logout_user()
    flash('您已经退出登录', 'success')
    return redirect(url_for('.index'))

@front.route('/register', methods=['GET', 'POST'])
def register():
    # 引入RegisterForm()表单
    form = RegisterForm()

    # validate_on_submit FlaskForm封装的方法，若提交的表单通过验证器验证，返回True,or False

    if form.validate_on_submit():
        if not form.username.data.isalnum():
            flash('username only support alphabet and digital', 'success')
        else:
            form.create_user()
            flash('注册成功，请登录！','success')
            return redirect(url_for('.login'))
    return render_template('register.html', form=form)
