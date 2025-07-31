from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_mail import Mail, Message
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash


def create_serializer(secret_key):
    """Create and return a serializer with the given secret key."""
    return URLSafeTimedSerializer(secret_key)

def generate_token(secret_key, email):
    """Generate a token for password reset."""
    serializer = create_serializer(secret_key)
    return serializer.dumps(email, salt="password-reset-salt")

def verify_token(secret_key, token, expiration=3600):
    """Verify the reset token and return the email if valid."""
    serializer = create_serializer(secret_key)
    try:
        # Try to load the email from the token
        email = serializer.loads(token, salt="password-reset-salt", max_age=expiration)
        print(f"Email from password reset salt: {email}")  # Debugging line
        return email
    except SignatureExpired:
        # Token has expired
        print("Token has expired")  # Debugging line
        return None
    except BadSignature:
        # Token is invalid or tampered with
        print("Invalid token signature")  # Debugging line
        return None
    except Exception as e:
        # General exception handling
        print(f"An error occurred: {str(e)}")
        return None

def hash_password(password):
    return generate_password_hash(password)

def check_password(password, hashed_password):
    return check_password_hash(hashed_password, password)

def send_reset_email(email, token):
    mail = Mail()
    msg = Message("Password Reset Request", sender="noreply@example.com", recipients=[email])
    reset_url = url_for("reset_password_view", token=token, _external=True)
    msg.body = f"To reset your password, visit the following link: {reset_url}"
    mail.send(msg)
