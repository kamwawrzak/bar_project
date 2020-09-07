from flask import Flask

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')
    db.init_app(app)

    with app.app_context():
        from . import routes  # noqa
        from .blueprints import register_bp
        app.register_blueprint(register_bp.register_bp)
        db.create_all()
        return app
