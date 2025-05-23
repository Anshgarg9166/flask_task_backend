### ✅ app/routes/tasks.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.models.task import TaskManager
from app.models.logger import TaskLogger
from app.extensions import db, limiter
from app.utils.role_required import role_required
from datetime import datetime
from app.schemas.task_schema import CreateTaskSchema, UpdateTaskSchema
from pydantic import ValidationError
import pandas as pd
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("/list", methods=["GET"])
@jwt_required()
@limiter.limit("10 per minute")
def get_tasks():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    tasks = TaskLogger.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify([
        {
            "id": t.id,
            "task_id": t.task_id,
            "status": t.status,
            "log_date": t.logged_at
        }
        for t in tasks.items
    ]), 200

@task_bp.route("/", methods=["GET"])
@jwt_required()
@limiter.limit("5 per minute")
def tasks_greeting():
    claims = get_jwt()
    return jsonify({
        "message": f"Hello {claims['username']} (Role: {claims['role']}), here are your tasks (secured)"
    }), 200

@task_bp.route("/by-date", methods=["GET"])
@jwt_required()
@limiter.limit("5 per minute")
def get_tasks_by_date():
    date = request.args.get("date")
    if not date:
        return jsonify({"error": "Date parameter is required"}), 400

    cache_key = f"tasks:{date}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return jsonify({"cached": True, "tasks": eval(cached_data)}), 200

    tasks = TaskLogger.query.filter(TaskLogger.logged_at.like(f"{date}%")).all()
    task_list = [
        {"id": t.id, "task_id": t.task_id, "status": t.status, "log_date": t.logged_at}
        for t in tasks
    ]
    redis_client.setex(cache_key, 3600, str(task_list))
    return jsonify({"cached": False, "tasks": task_list}), 200

@task_bp.route("/<int:task_logger_id>", methods=["GET"])
@jwt_required()
@limiter.limit("5 per minute")
def get_task_details(task_logger_id):
    task = TaskLogger.query.filter_by(id=task_logger_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({
        "id": task.id,
        "task_id": task.task_id,
        "status": task.status,
        "log_date": task.logged_at
    }), 200

@task_bp.route("/", methods=["POST"])
@jwt_required()
@limiter.limit("5 per minute")
def create_task():
    try:
        data = CreateTaskSchema(**request.get_json())
    except ValidationError as e:
        return jsonify(e.errors()), 400

    new_task = TaskManager(
        task_name=data.task_name,
        description=data.description,
        status=data.status,
        priority=data.priority,
        created_at=data.created_at,
        assigned_user=data.assigned_user
    )
    db.session.add(new_task)
    db.session.commit()

    log = TaskLogger(
        task_id=new_task.id,
        task_name=new_task.task_name,
        status=True
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "Task created"}), 201

@task_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
@limiter.limit("5 per minute")
def update_task(task_id):
    task = TaskManager.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    try:
        data = UpdateTaskSchema(**request.get_json())
    except ValidationError as e:
        return jsonify(e.errors()), 400

    task.task_name = data.task_name or task.task_name
    task.description = data.description or task.description
    task.status = data.status if data.status is not None else task.status
    task.priority = data.priority or task.priority
    task.assigned_user = data.assigned_user or task.assigned_user
    db.session.commit()

    log = TaskLogger(
        task_id=task.id,
        task_name=task.task_name,
        status=True
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "Task updated"}), 200

@task_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
@limiter.limit("5 per minute")
def soft_delete_task(task_id):
    task = TaskManager.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    task.status = False
    db.session.commit()

    log = TaskLogger(
        task_id=task.id,
        task_name=task.task_name,
        status=False
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "Task marked as inactive"}), 200

@task_bp.route("/upload-csv", methods=["POST"])
@jwt_required()
@role_required(["admin", "user"])
@limiter.limit("3 per minute")
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    try:
        df = pd.read_csv(file)
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    except Exception as e:
        return jsonify({"error": f"Failed to read CSV: {str(e)}"}), 400

    invalid_rows = df[df["created_at"].isna()]
    if not invalid_rows.empty:
        return jsonify({
            "error": "Some rows have invalid date format in 'created_at'",
            "invalid_rows": invalid_rows.to_dict(orient="records")
        }), 400

    for _, row in df.iterrows():
        task = TaskManager(
            task_name=row["task_name"],
            description=row["description"],
            status=str(row["status"]).strip().lower() == "true",
            priority=row["priority"],
            created_at=row["created_at"],
            assigned_user=row["assigned_user"]
        )
        db.session.add(task)
        db.session.flush()  # Get ID before commit

        log = TaskLogger(
            task_id=task.id,
            task_name=task.task_name,
            status=True
        )
        db.session.add(log)

    db.session.commit()
    return jsonify({"message": "CSV uploaded successfully"}), 201
