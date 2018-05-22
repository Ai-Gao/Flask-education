from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from simpledu.decorators import admin_required
from simpledu.models import Course, db, User, Live
from simpledu.forms import CourseForm, RegisterForm, UserForm, LiveForm, MessageForm
from flask_login import current_user
import json
from .ws import redis

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

# 课程路由
@admin.route('/courses')
@admin_required
def courses():
    page = request.args.get('page', default=1, type=int)
    pagination = Course.query.paginate(
            page=page,
            per_page=current_app.config['ADMIN_PER_PAGE'],
            error_out=False
            )
    return render_template('admin/courses.html', pagination=pagination)

# 添加课程路由
@admin.route('/courses/create', methods=['GET', 'POST'])
@admin_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        form.create_course()
        flash('课程创建成功', 'success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/create_courses.html', form=form)

# 编辑课程路由
@admin.route('/courses/<int:course_id>/edit', methods=['POST', 'GET'])
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    form.set_course(course)
    if form.validate_on_submit():
        form.update_course(course)
        flash('课程创建成功','success')
        redirect(url_for('admin.courses'))
    return render_template('admin/edit_courses.html', form=form, course=course)

    #if form.is_submitted():
    #    form.populate_obj(course)
    #    db.session.add(course)
    #    try:
    #        db.session.commit()
    #    except:
    #        flash('课程已经存在', 'danger')
    #        db.session.rollback()
    #    else:
    #        flash('课程修改成功', 'success')
    #        return redirect(url_for('admin.courses'))
    #return render_template('admin/edit_courses.html',form=form,course=course)

    """
    if form.validate_on_submit():
        form.update_course(course)
        flash('课程修改成功', 'success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/edit_courses.html', form=form, course=course)
    """

# 删除课程
@admin.route('/courses/<int:course_id>/delete')
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('课程删除成功', 'success')
    return redirect(url_for('admin.courses'))

# 管理用户路由
@admin.route('/users')
@admin_required
def users():
    page = request.args.get('page',default=1,type=int)
    pagination = User.query.paginate(
            page = page,
            per_page = current_app.config['ADMIN_PER_PAGE'],
            error_out=False
            )
    return render_template('admin/users.html', pagination=pagination)

# 增加用户
@admin.route('/users/create', methods=['GET','POST'])
@admin_required
def create_user():
    form = UserForm()
    #form = RegisterForm()
    if form.validate_on_submit():
            form.create_user()
            flash('课程创建成功', 'success')
            return redirect(url_for('admin.users'))
    return render_template('admin/create_users.html', form=form)


# 编辑用户
@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required

def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    #form = RegisterForm(obj=user)
    form = UserForm(obj=user)
    form.set_user(user)
    if form.validate_on_submit():
        form.update_user(user)
        flash('用户信息更新成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_user.html', form=form,user=user)

   # if form.validate_on_submit():
   #     form.populate_obj(user)
   #     db.session.add(user)
   #     try:
   #         db.session.commit()
   #     except:
   #         db.session.rollback()
   #         flash('用户名已经存在', 'danger')
   #     else:
   #         flash('用户信息更新成功', 'success')
   #         return redirect(url_for('admin.users'))
   # return render_template('admin/edit_user.html', form=form, user=user)



# 删除用户
@admin.route('/users/<int:user_id>/delete', methods=['POST', 'GET'])
@admin_required
def delete_user(user_id):
    if current_user.id == user_id:
        flash('用户不能自我删除','error')
        return redirect(url_for('admin.users'))
    user= User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('用户已经被删除', 'success')
    return redirect(url_for('admin.users'))

# 直播管理页面
@admin.route('/live')
@admin_required
def live():
    page = request.args.get('page', default=1,type=int)
    pagination = Live.query.paginate(
            page = page,
            per_page = current_app.config['ADMIN_PER_PAGE'],
            error_out=False
            )
    return render_template('admin/lives.html', pagination=pagination)

# 添加直播路由
@admin.route('/live/create', methods=['GET', 'POST'])
@admin_required
def create_live():
    form = LiveForm()
    if form.validate_on_submit():
        form.create_live()
        flash('直播创建成功', 'success')
        return redirect(url_for('admin.live'))
    return render_template('admin/create_lives.html', form=form)

# 添加后台信息管理路由
@admin.route('/message', methods=['GET','POST'])
@admin_required
def send_message():
    form = MessageForm()
    if form.validate_on_submit():
        redis.publish('chat', json.dumps(dict(username='System', text=form.text.data)))
        flash('系统消息发送成功', 'success')
        return redirect(url_for('admin.index'))
    return render_template('admin/message.html', form=form)

