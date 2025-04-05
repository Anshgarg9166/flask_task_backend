
from app.extensions import db
from datetime import datetime

class TaskManager(db.Model):
    __tablename__ = 'task_manager'
    
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    status = db.Column(db.Boolean, default=True)
    priority = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    assigned_user = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    user = db.relationship("User", back_populates="tasks", lazy="joined")

    def __repr__(self):
        return f"<Task {self.task_name}>"
