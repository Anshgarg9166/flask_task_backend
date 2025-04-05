from functools import wraps
from flask import request, jsonify
from app.models.user import User  # Assuming your User model has a role field

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Dummy authentication from headers (replace with real JWT validation)
            username = request.headers.get("X-User")
            if not username:
                return jsonify({"error": "Authentication required"}), 401

            user = User.query.filter_by(username=username).first()
            if not user or user.role not in allowed_roles:
                return jsonify({"error": "Unauthorized"}), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator
