MAIL_SERVER = 'smtp.example.com'  # Replace with your SMTP server
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'rayden.ai@gmail.com'
MAIL_PASSWORD = 'fjxu vbdr vwea gusu'
MAIL_DEFAULT_SENDER = 'noreply@example.com'
SECRET_KEY = 'your-flask-app-secret-key'  # For URLSafeTimedSerializer

# Flask-Mail Config (Use your SMTP settings)
# app.config["MAIL_SERVER"] = "smtp.gmail.com"
# app.config["MAIL_PORT"] = 587
# app.config["MAIL_USE_TLS"] = True
# app.config["MAIL_USERNAME"] = "your_email@gmail.com"
# app.config["MAIL_PASSWORD"] = "your_email_password"

# Then initialize Mail in your app:
# from flask_mail import Mail

# mail = Mail(app)