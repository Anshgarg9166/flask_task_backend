from app.extensions import db
from app.models import TaskManager, TaskLogger
from datetime import date
from celery_worker import celery

@celery.task
def daily_transfer_tasks():
    today = date.today()
    
    active_tasks = TaskManager.query.filter_by(status="active").all()
    
    for task in active_tasks:
        # Check if already logged for today
        already_logged = TaskLogger.query.filter_by(task_id=task.id, date=today).first()
        if already_logged:
            continue
        
        log = TaskLogger(
            task_id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            date=today
        )
        db.session.add(log)
    
    db.session.commit()
