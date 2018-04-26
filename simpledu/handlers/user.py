from flask import Blueprint, render_template, abort
from practice.models import User, Course

user = Blueprint('user', __name__,url_prefix='/user')

@user.route('/<arg>')
def index(arg):
    user = User.query.filter_by(username=arg).first_or_404()
    return render_template('user.html', user=user)
