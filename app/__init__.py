from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from celery.schedules import crontab

from app.routes.tasks import task_bp
from app.routes.auth import auth_bp
from app.extensions import db
from app.config import Config
from .celery import make_celery

# Extensions
migrate = Migrate()
jwt = JWTManager()
cache = Cache()
limiter = Limiter(key_func=get_remote_address)

celery = None  # Global celery instance


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    cache.init_app(app)
    limiter.init_app(app)

    # Import models (needed for migration)
    from app.models.user import User
    from app.models.task import TaskManager
    from app.models.logger import TaskLogger
    from app.models import events

    # Register routes
    app.register_blueprint(task_bp)
    app.register_blueprint(auth_bp)

    # Initialize Celery
    global celery
    celery = make_celery(app)

    # Register celery beat schedule
    celery.conf.beat_schedule = {
        'log-active-tasks-daily': {
            'task': 'app.tasks.daily_log.log_active_tasks_daily',
            'schedule': crontab(hour=0, minute=0),  # Every day at midnight
        }
    }

    return app
