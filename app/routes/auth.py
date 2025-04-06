from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt,
)
from app.extensions import db
from app.models.user import User
from app.utils.role_required import role_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# ========================
# Register a New User
# ========================
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    new_user = User(username=username, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# ========================
# User Login & Token Issuance
# ========================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "username": user.username,
            "role": user.role
        }
    )

    return jsonify({"access_token": access_token}), 200

# ========================
# Admin Only: List All Users
# ========================
@auth_bp.route("/users", methods=["GET"])
@jwt_required()
@role_required("admin")
def list_users():
    users = User.query.all()
    result = [
        {"id": user.id, "username": user.username, "role": user.role}
        for user in users
    ]
    return jsonify(result), 200
