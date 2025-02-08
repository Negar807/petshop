from flask import Flask, Blueprint
from app.controllers.home import home_bp
from app.controllers.auth import auth_bp
from app.controllers.user import user_bp
from app.controllers.admin import admin_bp
from app.controllers.payment import payment_bp


routes_bp = Blueprint('routes', __name__)

def register_routes(app: Flask):
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(payment_bp, url_prefix='/payment')
