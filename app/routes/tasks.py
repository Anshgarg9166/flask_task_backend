from flask import Blueprint, request, jsonify
import pandas as pd
from app.models.task import TaskManager, db

task_bp = Blueprint("tasks", __name__)

@task_bp.route("/upload-csv", methods=["POST"])
def upload_csv():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided"}), 400

    df = pd.read_csv(file)
    for _, row in df.iterrows():
        task = TaskManager(
            task_name=row["task_name"],
            description=row["description"],
            status=row["status"] == "True",
            priority=row["priority"],
            created_at=row["created_at"],
            assigned_user=row["assigned_user"]
        )
        db.session.add(task)

    db.session.commit()
    return jsonify({"message": "CSV file uploaded successfully!"}), 201
