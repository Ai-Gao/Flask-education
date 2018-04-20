from flask import Blueprint, render_template, abort
from practice.models import User, Course

user = Blueprint('user', __name__,url_prefix='/user')

@user.route('/<arg>')
def index(arg):
    if arg != 'admin':
        abort(404)
    users_info = User.query.all()
    publish_courses = Course.query.all()
    return render_template('user.html', users_info=users_info, publish_courses=publish_courses)
