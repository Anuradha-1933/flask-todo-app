from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Task

tasks_bp = Blueprint("tasks", __name__, template_folder="../templates")

@tasks_bp.route("/tasks")
def view_tasks():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    tasks = Task.query.order_by(Task.id.desc()).all()
    return render_template("tasks.html", tasks=tasks)

@tasks_bp.route("/tasks/add", methods=["POST"])
def add_task():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    title = request.form.get("title", "").strip()
    if title:
        task = Task(title=title, status="Pending")
        db.session.add(task)
        db.session.commit()
        flash("Task added.", "success")
    else:
        flash("Title cannot be empty.", "danger")
    return redirect(url_for("tasks.view_tasks"))

@tasks_bp.route("/tasks/toggle/<int:task_id>", methods=["POST"])
def toggle_status(task_id):
    if "user" not in session:
        return redirect(url_for("auth.login"))

    task = Task.query.get_or_404(task_id)
    if task.status == "Pending":
        task.status = "Working"
    elif task.status == "Working":
        task.status = "Done"
    else:
        task.status = "Pending"
    db.session.commit()
    flash("Task updated.", "info")
    return redirect(url_for("tasks.view_tasks"))

@tasks_bp.route("/tasks/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if "user" not in session:
        return redirect(url_for("auth.login"))

    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "info")
    return redirect(url_for("tasks.view_tasks"))

@tasks_bp.route("/tasks/clear", methods=["POST"])
def clear_tasks():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    Task.query.delete()
    db.session.commit()
    flash("All tasks cleared.", "info")
    return redirect(url_for("tasks.view_tasks"))
