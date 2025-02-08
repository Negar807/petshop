from flask import render_template, Blueprint
from app.models import Dog

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
    dogs = Dog.query.all()
    return render_template('index.html',dogs=dogs)