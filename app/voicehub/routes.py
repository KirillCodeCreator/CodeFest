from flask import Blueprint, redirect, render_template, request
from flask_login import login_required, login_user

from app.models import db_session
from app.models.users import Users

voicehub = Blueprint(
    "voicehub",
    __name__,
    template_folder="../../src/public",
    static_folder="../../src/public",
)
db_session.global_init("app/app.db")
db_ses = db_session.create_session()


@voicehub.route(
    "/",
    methods=[
        "POST",
        "GET",
    ],
)
def index():
    # return render_template("index.html", title="VoiceHub")
    return render_template("index.html")


@voicehub.route(
    "/login",
    methods=[
        "POST",
        "GET",
    ],
)
def login():
    if request.method == "POST":
        user_data = request.form
        user = (
            db_ses.query(Users)
            .filter(Users.email == user_data["email"])
            .first()
        )
        if user and user.check_password(user_data["password"]):
            login_user(user, remember=True)
            return redirect("/")
        return render_template(
            "login.html", error="Неправильный логин или пароль"
        )
    return render_template("login.html")


@voicehub.route(
    "/logout",
    methods=[
        "POST",
        "GET",
    ],
)
@login_required
def logout():
    pass


@voicehub.route(
    "/register",
    methods=[
        "POST",
        "GET",
    ],
)
def register():
    pass


@voicehub.route(
    "/chat",
    methods=[
        "POST",
        "GET",
    ],
)
@login_required
def chat():
    uuid = request.args.get("uuid", default=None, type=str)
    return uuid
