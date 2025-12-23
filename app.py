# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

from auth.models import db, login_manager   # import single instances


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "change_this_to_strong_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "static", "uploads")
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # init extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from auth.routes import auth_bp
    from utils.routes import utils_bp
    from auth.models import User   # safe now

    app.register_blueprint(auth_bp)
    app.register_blueprint(utils_bp)

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
