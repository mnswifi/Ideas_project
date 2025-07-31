from flask import abort
from flask_login import current_user
from functools import wraps

def role_required(allowed_roles):
    """
    Decorator to restrict access to users with specific roles.
    
    Usage:
    @role_required(["admin", "superadmin"])
    def some_view():
        ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return abort(401)  # Unauthorized

            if current_user.role not in allowed_roles:
                return abort(403)  # Forbidden

            return f(*args, **kwargs)
        return decorated_function
    return decorator
