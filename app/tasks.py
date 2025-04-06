from celery_worker import celery
from app.models import Task  # Replace with your actual model import
from app import db

@celery.task
def transfer_active_tasks():
    active_tasks = Task.query.filter_by(status='active').all()
    for task in active_tasks:
        # Do your transfer logic here (e.g., archive, send to another table, etc.)
        task.status = 'archived'  # Example change
    db.session.commit()
    print(f"Transferred {len(active_tasks)} active tasks.")
