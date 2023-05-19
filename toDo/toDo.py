from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from toDo.auth import login_required
from toDo.db import get_db

bp = Blueprint("toDo", __name__)


@bp.route("/", methods=["GET"])
# @login_required
def index():
    db, c = get_db()

    c.execute(
        f"""SELECT t.id, t.description, u.username, t.completed, t.created_at 
        FROM toDo t 
        JOIN user u ON t.created_by = u.id 
        ORDER BY t.created_at DESC"""
    )

    toDos = c.fetchall()

    return render_template("toDo/index.html", toDos=toDos)


@bp.route("/update", methods=["GET", "POST"])
@login_required
def update():
    return "Update working", 200


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    return "Create working", 200
