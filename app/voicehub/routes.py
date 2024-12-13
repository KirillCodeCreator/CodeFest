from flask import Blueprint, redirect, render_template, request
from flask_login import current_user, login_required, login_user, logout_user

from app.models import db_session
from app.models.users import Users

voicehub = Blueprint(
    "voicehub",
    __name__,
    template_folder="../../src/public/html",
    static_folder="../../src/public/styles",
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
    if current_user.is_authenticated:
        return render_template("main-page.html", user=current_user)
    else:
        return redirect("/login")


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
    logout_user()
    return redirect("/login")


@voicehub.route(
    "/registration",
    methods=[
        "POST",
        "GET",
    ],
)
def register():
    if request.method == "POST":
        user_data = request.form
        if db_ses.query(Users).filter_by(email=user_data["email"]).first():
            return render_template(
                "registration.html",
                error="Пользователь с таким email уже есть!",
            )
        elif len(user_data["password"]) < 8:
            return render_template(
                "registration.html",
                error="Длина пароля должна быть не менее 8 символов!",
            )
        elif user_data["password"] != user_data["repeatpassword"]:
            return render_template(
                "registration.html",
                error="Пароли не совпадают!",
            )
        user = Users(
            name=user_data["name"],
            email=user_data["email"],
        )
        print(user_data["password"])
        user.set_password(user_data["password"])
        db_ses.add(user)
        db_ses.commit()
        return redirect("/login")
    return render_template("registration.html")


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
