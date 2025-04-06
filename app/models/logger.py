from app.extensions import db
from datetime import datetime

class TaskLogger(db.Model):
    __tablename__ = "task_logger"

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task_manager.id", ondelete="CASCADE"), nullable=False)
    task_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<TaskLog {self.task_name}>"
