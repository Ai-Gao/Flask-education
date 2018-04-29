from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from simpledu.decorators import admin_required
from simpledu.models import Course, db
from simpledu.forms import CourseForm
admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

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
        flash('课程创建成功', 'sucess')
        return redirect(url_for('admin.courses'))
    return render_template('admin/create_courses.html', form=form)

# 编辑课程路由
@admin.route('/courses/<int:course_id>/edit', methods=['POST', 'GET'])
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        form.update_course()
        flash('课程修改成功', 'success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/edit_courses.html', form=form, course=course)

# 删除课程
@admin.route('/courses/<int:course_id>/delete')
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('课程删除成功', 'success')
    return redirect(url_for('admin.courses'))
