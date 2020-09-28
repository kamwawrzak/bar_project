from flask import Flask

from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
lm = LoginManager()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')
    db.init_app(app)
    lm.init_app(app)

    with app.app_context():
        from .blueprints import (comment_bp, login_bp, drink_bp, home_bp,
                                 profile_bp, register_bp, search_bp)
        app.register_blueprint(home_bp.home_bp)
        app.register_blueprint(login_bp.login_bp)
        app.register_blueprint(drink_bp.drink_bp)
        app.register_blueprint(register_bp.register_bp)
        app.register_blueprint(search_bp.search_bp)
        app.register_blueprint(profile_bp.profile_bp)
        app.register_blueprint(comment_bp.comment_bp)
        db.create_all()
        return app
