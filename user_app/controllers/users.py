from user_app import app
from user_app.models.user import User
from flask import render_template, redirect, request, session, flash
from user_app import bcrypt


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/register")
def create_user():
    if not User.check_if_reg(request.form):
        return redirect("/")

    potential_user = User.get_by_email(request.form["email"])

    if potential_user:
        flash("Email in use, Please Log in", "register")
        return redirect("/")

    pw = bcrypt.generate_password_hash(request.form["password"])

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw,
    }

    user_id = User.create(data)

    session["user_id"] = user_id
    return redirect("/dashboard")


@app.post("/login")
def login():
    if not User.check_if_login(request.form):
        return redirect("/")

    potential_user = User.get_by_email(request.form["email"])

    if not potential_user:
        flash("invalid Email or Password", "login")
        return redirect("/")

    user = potential_user
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("invalid Email or Password", "login")
        return redirect("/")

    session["user_id"] = user.id

    return redirect("/dashboard")


@app.get("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.get("/dashboard")
def display_dash():
    if "user_id" not in session:
        return redirect("/")
    user = User.get_by_id(session["user_id"])

    return render_template("dashboard.html", user=user)
