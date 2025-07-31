from flask import render_template, Response, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from facerecognition import display_in_browser
from auth import login, logout, forgot_password, reset_password, register_user, register_staff
from models import User
from bson import ObjectId
from datetime import datetime, timedelta
from utils import verify_token, hash_password
from decorators import role_required


# Configure routes
def configure_routes(app, mongo, socketio, bcrypt, login_manager):
    # Set the login view for Flask-Login redirection
    login_manager.login_view = "login_view"

    # User Loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        return User(user_data) if user_data else None
    
    # Home route
    @app.route("/")
    def home():
        return render_template("index.html")

    # Admin Home route
    @app.route("/home")
    @login_required
    @role_required(["admin", "director"])
    def admin_home():
        today_date = datetime.now().strftime('%d/%m/%Y')
        attendance = mongo.db.attendance.find({"time_in": {"$regex": f"^{today_date}"}})
        attendance_list = []
        for record in attendance:
            time_in = datetime.strptime(record['time_in'], '%d/%m/%Y %H:%M')
            time_out = record.get('time_out')
            if time_out:
                time_out = datetime.strptime(time_out, '%d/%m/%Y %H:%M')
                total_seconds = (time_out - time_in).total_seconds()
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                if hours > 0:
                    record['hours_worked'] = f"{hours} hour{'s' if hours > 1 else ''} and {minutes} minute{'s' if minutes > 1 else ''}"
                else:
                    record['hours_worked'] = f"{minutes} minute{'s' if minutes > 1 else ''}"
            else:
                record['hours_worked'] = 'N/A'
            attendance_list.append(record)
        return render_template("admin_home.html", attendance_list=attendance_list)

    # Login routes
    @app.route("/login", methods=["GET", "POST"])
    def login_view():
        return login(mongo)

    @app.route("/logout")
    @login_required
    def logout_view():
        return logout()

    # Password routes
    @app.route("/forgot_password", methods=["GET", "POST"])
    def forgot_password_view():
        return forgot_password(mongo)

    @app.route("/reset_password", methods=["GET", "POST"])
    def reset_password_view():
        token = request.args.get("token")
        return render_template("reset_password.html")
    
    @app.route("/change_password", methods=["GET", "POST"])
    def change_password_view():
        token = request.form["token"]
        return reset_password(mongo, bcrypt, token)

    # Dashboard route
    @app.route("/dashboard")
    @login_required
    @role_required(["admin", "director"])
    def dashboard():
        return render_template("dashboard.html")

    # Admin Login and Registration routes
    @app.route("/adlogin")
    @login_required
    @role_required(["admin", "director"])
    def adlogin():
        return render_template("adlogin.html")

    @app.route("/adregister", methods=["GET", "POST"])
    def adregister():
        return render_template("adregister.html")

    # Analytics route
    @app.route("/analytics")
    @login_required
    @role_required(["director"])
    def analytics():
        return render_template("analytics.html")

    # User registration route
    @app.route("/register", methods=["GET", "POST"])
    def register_view():
        return register_user(mongo)

    # Staff Registration route
    @app.route("/staff_registration")
    def staff_reg():
        return render_template("staff_registration.html")

    # Video feed route for streaming
    @app.route('/video_feed')
    def video_feed():
        """Route to stream video frames."""
        return Response(display_in_browser(mongo, socketio), mimetype='multipart/x-mixed-replace; boundary=frame')

