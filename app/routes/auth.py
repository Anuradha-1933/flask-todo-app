from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint("auth", __name__, template_folder="../templates")

# Demo credentials (replace with real auth later)
user_credentials = {"username": "admin", "password": "admin"}

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == user_credentials["username"] and password == user_credentials["password"]:
            session["user"] = username
            flash("Login successful.", "success")
            return redirect(url_for("tasks.view_tasks"))
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for("auth.login"))

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out.", "info")
    return redirect(url_for("auth.login"))
