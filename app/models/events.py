# app/models/events.py

from datetime import datetime
from app.models.logger import TaskLogger
from sqlalchemy import event

def log_task_create(mapper, connection, target):
    connection.execute(TaskLogger.__table__.insert().values(
        task_id=target.id,
        task_name=target.task_name,
        status=target.status,
        logged_at=datetime.utcnow()  # ✅ Match your model field
    ))

def log_task_update(mapper, connection, target):
    connection.execute(TaskLogger.__table__.insert().values(
        task_id=target.id,
        task_name=target.task_name,
        status=target.status,
        logged_at=datetime.utcnow()  # ✅ Match your model field
    ))
