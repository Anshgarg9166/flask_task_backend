# app/__init__.py

from flask import Flask
# from app.models import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.routes.tasks import task_bp
from app.routes.auth import auth_bp
from app.models.logger import TaskLogger

from app.extensions import db


migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    app.config["DEBUG"] = True

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Import models only after db is initialized
    from app.models.user import User
    from app.models.task import TaskManager

    # Register routes
    
    app.register_blueprint(task_bp)
    app.register_blueprint(auth_bp)

    return app
