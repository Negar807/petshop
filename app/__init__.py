from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()


@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)



    from app.routes import register_routes
    register_routes(app)


    return app