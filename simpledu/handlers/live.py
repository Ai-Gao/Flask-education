from flask import Blueprint, render_template
from simpledu.forms import LiveForm

live = Blueprint('live', __name__, url_prefix='/live')

@live.route('/')
def index():
    form = LiveForm()
    return render_template('live/index.html', form=form)
