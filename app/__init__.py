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
        from . import routes  # noqa
        from .blueprints import login_bp, register_bp
        app.register_blueprint(login_bp.login_bp)
        app.register_blueprint(register_bp.register_bp)
        db.create_all()
        return app
