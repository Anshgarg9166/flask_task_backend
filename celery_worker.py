from celery import Celery
from celery.schedules import crontab
from app import create_app
import os

flask_app = create_app()
flask_app.app_context().push()

celery = Celery(__name__)
celery.config_from_object(flask_app.config, namespace='CELERY')
celery.autodiscover_tasks(['app.tasks'])

# Add Celery Beat schedule
celery.conf.beat_schedule = {
    'transfer-active-tasks-daily': {
        'task': 'app.tasks.transfer_active_tasks',
        'schedule': crontab(hour=0, minute=0),  # Every day at midnight
    },
}
