from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user
from models import User
from utils import hash_password, check_password, generate_token, send_reset_email, verify_token


def check_existing_email(mongo, email):
    return mongo.db.users.find_one({"email": email}) is not None


def login(mongo):
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user_data = mongo.db.users.find_one({"email": email})

        if user_data and check_password(password, user_data["password"]):
            user = User(user_data)
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid email or password", "danger")
    return render_template("login.html")


def logout():
    logout_user()
    return redirect(url_for("login_view"))


def forgot_password(mongo):
    """Handle the password reset process by sending a reset link."""
    if request.method == "POST":
        email = request.form["email"]
        user = mongo.db.users.find_one({"email": email})

        if user:
            # Generate the reset token using the app's SECRET_KEY
            token = generate_token(current_app.config['SECRET_KEY'], email)
            mongo.db.users.update_one({"email": email}, {"$set": {"reset_token": token}})
            send_reset_email(email, token)
            flash("Password reset link sent to your email", "info")
        else:
            flash("Email not found", "danger")

    return render_template("forgot_password.html")

def reset_password(mongo, bcrypt, token):
    """Reset the user's password after verifying the token."""
    email = verify_token(current_app.config['SECRET_KEY'], token)
    if not email or "@" not in email:
        flash("Invalid or expired token", "danger")
        return redirect(url_for("login_view"))
    
    user = mongo.db.users.find_one({"email": email, "reset_token": token})
    if not user:
        flash("Invalid or expired token", "danger")
        return redirect(url_for("login_view"))
    
    if request.method == "POST":
        new_password = request.form["password"]
        hashed_password = hash_password(new_password)

        # Update the password in the database
        result = mongo.db.users.update_one({"email": email}, {"$set": {"password": hashed_password}, "$unset": {"reset_token": ""}})
        if result.modified_count == 1:
            flash("Password updated successfully!", "success")
        else:
            flash("Failed to update password. Please try again.", "danger")
        return redirect(url_for("login_view"))

    return render_template("reset_password.html", email=email)

def register_user(mongo):
    """Register a new user with the provided details."""
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        directorate = request.form["directorate"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        # Ensure the role is valid
        allowed_roles = ["staff", "admin", "director"]
        if role not in allowed_roles:
            flash("You cannot assign this role!", "danger")
            return redirect(url_for("register_view"))

        # Ensure unique email
        if check_existing_email(mongo, email):
            flash("Email already registered.", "danger")
            return redirect(url_for("register_view"))

        # Hash the password before saving to the database
        hashed_password = hash_password(password)

        # Insert the new user into the database
        mongo.db.users.insert_one({
            "first_name": first_name,
            "last_name": last_name,
            "directorate": directorate,
            "email": email,
            "password": hashed_password,
            "role": role
        })

        flash("Account created successfully!", "success")
        return redirect(url_for("login_view"))

    return render_template("adregister.html")

def register_staff(mongo):
    if request.method == "POST":
        first_name = request.form.get("firstname", "").strip()
        last_name = request.form.get("lastname", "").strip()
        directorate = request.form.get("directorate", "").strip()
        staff_Id = request.form.get("staff_Id", "").strip()
        appointment = request.form.get("appointment", "").strip()
        rfid_tag = request.form.get("rfid_tag", "").strip()

        # Validate empty fields
        if not all([first_name, last_name, directorate, staff_Id, appointment, rfid_tag]):
            flash("All fields are required!", "danger")
            return redirect(url_for("register_view"))
        
        # Ensure unique staff ID
        existing_user = mongo.db.users.find_one({"staff_Id": staff_Id})
        if existing_user:
            flash("Staff with this staff ID already exists.", "danger")
            return redirect(url_for("register_view"))
        
        # Ensure unique RFID Tag
        if not rfid_tag:
            flash("RFID Tag is required!", "danger")
            return redirect(url_for("register_view"))

        existing_rfid_tag = mongo.db.users.find_one({"rfid_Tag": rfid_tag})
        if existing_rfid_tag:
            flash("RFID Tag already exists.", "danger")
            return redirect(url_for("register_view"))
        
        # Store user in MongoDB
        mongo.db.users.insert_one({
            "first_name": first_name,
            "last_name": last_name,
            "directorate": directorate,
            "staff_Id": staff_Id,
            "appointment": appointment,
            "rfid_Tag": rfid_tag

        })

        flash("Staff registered successfully!", "success")
        return redirect(url_for("register_view"))

    return render_template("register.html")