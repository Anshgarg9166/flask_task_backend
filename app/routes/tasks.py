from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.task import TaskManager
from app.models.logger import TaskLogger
from app.extensions import db
from app.utils.role_required import role_required
from datetime import datetime
import pandas as pd
import redis

# Initialize Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Blueprint with URL prefix
task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# ====================
# ROUTES
# ====================

# Paginated Tasks (GET /tasks/list)
@task_bp.route("/list", methods=["GET"])
@jwt_required()
def get_tasks():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    tasks = TaskLogger.query.paginate(page=page, per_page=per_page, error_out=False)
    tasks_list = [
        {"id": t.id, "task_id": t.task_id, "status": t.status, "log_date": t.log_date}
        for t in tasks.items
    ]
    return jsonify(tasks_list), 200

# Filter by Date (GET /tasks/by-date?date=2024-04-05)
@task_bp.route("/by-date", methods=["GET"])
@jwt_required()
def get_tasks_by_date():
    date = request.args.get("date")
    if not date:
        return jsonify({"error": "Date parameter is required"}), 400

    cache_key = f"tasks:{date}"
    cached_data = redis_client.get(cache_key)

    if cached_data:
        return jsonify({"cached": True, "tasks": eval(cached_data)}), 200

    tasks = TaskLogger.query.filter(TaskLogger.log_date.like(f"{date}%")).all()
    tasks_list = [
        {"id": t.id, "task_id": t.task_id, "status": t.status, "log_date": t.log_date}
        for t in tasks
    ]

    redis_client.setex(cache_key, 3600, str(tasks_list))  # Cache for 1 hour
    return jsonify({"cached": False, "tasks": tasks_list}), 200

# Authenticated user test route (GET /tasks/)
@task_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks_message():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello {current_user['id']}, here are your tasks (secured)"}), 200

# Protected route test (GET /tasks/protected)
@task_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello, user {current_user['id']}. You are authenticated!"}), 200

# Upload Tasks via CSV (POST /tasks/upload-csv)
@task_bp.route("/upload-csv", methods=["POST"])
@jwt_required()
@role_required(['admin', 'user']) 
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    try:
        df = pd.read_csv(file)
    except Exception as e:
        return jsonify({"error": f"Failed to read CSV: {str(e)}"}), 400

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

# Admin-only route (GET /tasks/admin-only)
@task_bp.route("/admin-only", methods=["GET"])
@jwt_required()
@role_required("admin")
def admin_route():
    return jsonify({"message": "Welcome, admin!"}), 200

# User-only route (GET /tasks/user-only)
@task_bp.route("/user-only", methods=["GET"])
@jwt_required()
@role_required("user")
def user_route():
    return jsonify({"message": "Welcome, user!"}), 200
