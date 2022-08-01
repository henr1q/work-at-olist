from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    with app.app_context():
        from flask_api.routes import api_bp
        from flask_api.manage import cli

        app.register_blueprint(api_bp)
        app.register_blueprint(cli)

        from flask_api.models import db
        db.init_app(app)

        return app

