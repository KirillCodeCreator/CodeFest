import base64
import os

from flask import Blueprint, jsonify, redirect, render_template, request
from flask_login import current_user, login_required, login_user, logout_user

from app.models import db_session
from app.models.users import Users
from app.whisper.voice2text import voice2text_function

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


@voicehub.route("/get-voice2text", methods=["POST", "GET"])
def get_voice2text():
    data = request.json.get("data")

    if data is None:
        return jsonify({"error": "No data provided"}), 400

    try:
        # Декодирование base64 обратно в бинарные данные
        decoded_data = base64.b64decode(data)

        # Распознавание речи
        transcription = voice2text_function(decoded_data)

        return jsonify({"transcription": transcription})
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500


@voicehub.route("/save-audio", methods=["POST"])
def save_audio():
    data = request.json.get("data")
    fileName = request.json.get("fileName")

    if data is None or fileName is None:
        return jsonify({"error": "No data or file name provided"}), 400

    try:
        # Декодирование base64 обратно в бинарные данные
        decoded_data = base64.b64decode(data)

        # Создание папки cache, если она не существует
        cache_dir = "./app/cache"
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        # Сохранение файла в папке cache
        file_path = os.path.join(cache_dir, fileName)
        with open(file_path, "wb") as audio_file:
            audio_file.write(decoded_data)

        return jsonify({"message": "File saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
