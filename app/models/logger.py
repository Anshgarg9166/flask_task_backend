from app.extensions import db

class TaskLogger(db.Model):
    __tablename__ = "task_logger"

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer)
    task_name = db.Column(db.String(100))
    status = db.Column(db.Boolean)
    logged_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"<TaskLog {self.task_name}>"
