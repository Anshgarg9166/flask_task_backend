from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)

            if not user or user.role != required_role:
                return jsonify({"error": "Access forbidden: Insufficient role"}), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper
