import os
from celery.schedules import crontab

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change_this_key")

    # Redis Caching
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    CACHE_REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

    # Celery
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

CELERYBEAT_SCHEDULE = {
    'daily-task-transfer': {
        'task': 'app.tasks.celery_tasks.daily_transfer_tasks',
        'schedule': crontab(hour=0, minute=0),
    },
}

