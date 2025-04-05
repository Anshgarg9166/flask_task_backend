from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import pandas as pd

from app.utils import role_required  # Utility for RBAC
from datetime import datetime
import redis
from app.models.task import TaskManager
from app.models.logger import TaskLogger

from app.extensions import db
from app.utils import role_required




task_bp = Blueprint("tasks", __name__)

# Redis cache for optimized queries
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Upload CSV API
@task_bp.route("/upload-csv", methods=["POST"])
@jwt_required()
@role_required(["admin"])  # Only admins can upload tasks
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    df = pd.read_csv(file)

    for _, row in df.iterrows():
        task = TaskManager(
            task_name=row["task_name"],
            description=row["description"],
            status=str(row["status"]).strip().lower() == "true",
            priority=row["priority"],
            created_at=datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S"),
            assigned_user=row["assigned_user"]
        )
        db.session.add(task)

    db.session.commit()
    return jsonify({"message": "CSV uploaded successfully"}), 201

# GET all tasks (Paginated)
# @task_bp.route("/tasks", methods=["GET"])
# @jwt_required()
# def get_tasks():
#     page = request.args.get("page", 1, type=int)
#     per_page = request.args.get("per_page", 10, type=int)
    
#     tasks = TaskLogger.query.paginate(page=page, per_page=per_page, error_out=False)
#     return jsonify([{"id": task.id, "task_id": task.task_id, "status": task.status, "log_date": task.log_date} for task in tasks.items])

# GET tasks filtered by date (Cached)
@task_bp.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks_by_date():
    date = request.args.get("date")
    if not date:
        return jsonify({"error": "Date parameter is required"}), 400

    cache_key = f"tasks:{date}"
    cached_data = redis_client.get(cache_key)

    if cached_data:
        return jsonify({"cached": True, "tasks": eval(cached_data)})

    tasks = TaskLogger.query.filter(TaskLogger.log_date.like(f"{date}%")).all()
    tasks_list = [{"id": task.id, "task_id": task.task_id, "status": task.status, "log_date": task.log_date} for task in tasks]

    redis_client.setex(cache_key, 3600, str(tasks_list))  # Cache for 1 hour
    return jsonify({"cached": False, "tasks": tasks_list})

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    return jsonify({
        "message": f"Hello {current_user['id']}, here are your tasks (secured)"
    }), 200
    
@task_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()  # will be a string
    return jsonify({
        "message": f"Hello, user {current_user_id}. You are authenticated!"
    }), 200