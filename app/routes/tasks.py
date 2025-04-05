# from flask import Blueprint, request, jsonify
# import pandas as pd
# from app.models.task import TaskManager, db

# task_bp = Blueprint("tasks", __name__)

# @task_bp.route("/upload-csv", methods=["POST"])
# def upload_csv():
#     file = request.files.get("file")
#     if not file:
#         return jsonify({"error": "No file provided"}), 400

#     df = pd.read_csv(file)
#     for _, row in df.iterrows():
#         task = TaskManager(
#             task_name=row["task_name"],
#             description=row["description"],
#             status=row["status"] == "True",
#             priority=row["priority"],
#             created_at=row["created_at"],
#             assigned_user=row["assigned_user"]
#         )
#         db.session.add(task)

#     db.session.commit()
#     return jsonify({"message": "CSV file uploaded successfully!"}), 201
from flask import Blueprint, request, jsonify
import pandas as pd
from app.models.task import TaskManager, db
from datetime import datetime

task_bp = Blueprint("tasks", __name__)

@task_bp.route("/upload-csv", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    try:
        df = pd.read_csv(file)

        # Ensure required columns exist
        required_columns = {"task_name", "description", "status", "priority", "created_at", "assigned_user"}
        if not required_columns.issubset(df.columns):
            return jsonify({"error": "CSV missing required columns"}), 400

        inserted_tasks = []

        for _, row in df.iterrows():
            try:
                task = TaskManager(
                    task_name=row["task_name"],
                    description=row["description"],
                    status=str(row["status"]).strip().lower() == "true",
                    priority=row["priority"],
                    created_at=datetime.strptime(row["created_at"], "%m/%d/%Y"),
                    assigned_user=row["assigned_user"]
                )
                db.session.add(task)

                # Append data for response
                inserted_tasks.append({
                    "task_name": task.task_name,
                    "description": task.description,
                    "status": task.status,
                    "priority": task.priority,
                    "created_at": task.created_at,
                    "assigned_user": task.assigned_user
                })
            except Exception as e:
                return jsonify({"error": f"Error processing row: {str(e)}"}), 400

        db.session.commit()

        return jsonify({
            "message": "CSV file uploaded successfully!",
            "inserted_tasks": inserted_tasks
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@task_bp.route("/tasks", methods=["GET"])
def get_all_tasks():
    try:
        tasks = TaskManager.query.all()  # Fetch all tasks from the database

        # Convert query results into a list of dictionaries
        task_list = [
            {
                "id": task.id,
                "task_name": task.task_name,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "assigned_user": task.assigned_user,
            }
            for task in tasks
        ]

        return jsonify({"tasks": task_list}), 200  # Return tasks as JSON

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors