from celery import shared_task
from app.extensions import db
from app.models.task import TaskManager
from app.models.logger import TaskLogger
from datetime import datetime, date

@shared_task
def log_active_tasks_daily():
    today = date.today()

    active_tasks = TaskManager.query.filter_by(status=True).all()

    for task in active_tasks:
        already_logged = TaskLogger.query.filter(
            TaskLogger.task_id == task.id,
            db.func.date(TaskLogger.logged_at) == today
        ).first()

        if not already_logged:
            log = TaskLogger(
                task_id=task.id,
                task_name=task.task_name,
                status=task.status,
                logged_at=datetime.utcnow()
            )
            db.session.add(log)

    db.session.commit()
    return "Daily active task log complete."
