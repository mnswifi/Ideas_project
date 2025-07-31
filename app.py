import os
from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_mail import Mail, Message
import webbrowser
from dotenv import load_dotenv
from routes import configure_routes  # Import function to configure routes

load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app)


# MongoDB Configuration
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://192.168.1.114:27017/Play_Attendance")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "12345!@#")

# Mongo & Security Setup
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Flask-Mail Config
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

# Register routes
configure_routes(app, mongo, socketio, bcrypt, login_manager)

@app.errorhandler(403)
def forbidden(error):
    return render_template("403.html"), 403

@app.errorhandler(401)
def unauthorized(error):
    return render_template("401.html"), 401

@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500

if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:8001/')
    app.run('0.0.0.0',port=8001, debug=True)
