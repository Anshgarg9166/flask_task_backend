from flask import Flask
from app.utils.database import db
from app.config import Config
from app.routes.tasks import task_bp  # Import Blueprint inside the function

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Register Blueprints inside the function
    app.register_blueprint(task_bp, url_prefix="/api")
    app.config['DEBUG'] = True


    return app
