import base64
import datetime
import os
import uuid
from uuid import UUID

import sqlalchemy
from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.orm.attributes import flag_modified

from app.models import db_session
from app.models.chats_of_users import ChatsOfUsers
from app.models.solvings_of_problems import SolvingsOfProblems
from app.models.users import Users
from app.voicehub.functions.censor_users_text import censor_users_text_function
from app.voicehub.functions.check_censored_text_and_get_answer import (
    check_censored_text_function,
)
from app.voicehub.functions.find_best_solve_of_problem import (
    find_best_solve_of_problem,
)
from app.voicehub.functions.make_treatment_of_user import (
    add_treatment_to_data_base_function,
)
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
        list_of_users_chats = (
            db_ses.query(ChatsOfUsers).filter_by(user_id=current_user.id).all()
        )
        return render_template(
            "index.html",
            user=current_user,
            list_of_users_chats=list_of_users_chats,
        )
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


@voicehub.route("/save-audio", methods=["POST"])
def save_audio():
    data = request.json.get("data")
    fileName = request.json.get("fileName")
    chat_id = request.json.get("chat_id")

    chat = db_ses.query(ChatsOfUsers).filter_by(chat_id=UUID(chat_id))
    if chat:
        chat = chat.first()
    else:
        return "Chat not found", 404

    if data is None or fileName is None:
        return jsonify({"error": "No data or file name provided"}), 400

    try:
        decoded_data = base64.b64decode(data)
        cache_dir = "./app/cache"
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        file_path = os.path.join(cache_dir, fileName)
        with open(file_path, "wb") as audio_file:
            audio_file.write(decoded_data)
        transcription = voice2text_function(file_path=file_path)
        os.remove(file_path)
        print(transcription)
        transcription = censor_users_text_function(transcription)
        print(transcription)
        if transcription["complaint"] == "False":
            message_from_bot = check_censored_text_function(
                transcription["text"]
            )
        else:
            solvings_of_problems = list(
                map(
                    lambda x: x.solving_of_problem,
                    db_ses.query(SolvingsOfProblems).all(),
                )
            )
            print(solvings_of_problems)
            message_from_bot = find_best_solve_of_problem(
                problem=transcription["text"],
                solvings=solvings_of_problems,
            )
        chat.add_new_message(
            sender=current_user.name,
            content=transcription,
            datetime_of_users_message=datetime.datetime.now().isoformat(),
        )
        chat.add_new_message(
            sender="VoiceHubSupportBot",
            content=message_from_bot,
            datetime_of_users_message=datetime.datetime.now().isoformat(),
        )
        flag_modified(chat, "data")

        print(
            add_treatment_to_data_base_function(
                user_id=current_user.id,
                treatment=transcription["text"],
                db_session=db_ses,
            )
        )

        return jsonify(
            {
                "transcription": transcription["text"],
                "answer": message_from_bot,
            }
        )
    except Exception as e:
        print({"error", str(e)})
        return jsonify({"error": str(e)}), 500


@voicehub.route("/add-new-chat", methods=["POST", "GET"])
@login_required
def add_new_chat():
    name_of_chat = request.args.get("name", type=str)
    if not name_of_chat:
        return "Name of chat is required", 400
    new_chat_id = uuid.uuid4()
    chat = ChatsOfUsers(
        user_id=current_user.id,
        chat_id=new_chat_id,
        name_of_chat=name_of_chat,
    )

    try:
        db_ses.add(chat)
        db_ses.commit()
        return redirect(f"/chat?chat_id={str(new_chat_id)}")
    except sqlalchemy.exc.IntegrityError as e:
        db_ses.rollback()
        return f"Integrity Error: {e.orig}", 400
    except sqlalchemy.exc.SQLAlchemyError as e:
        db_ses.rollback()
        return f"SQLAlchemy Error: {e}", 500
    except Exception as e:
        db_ses.rollback()
        return f"Internal Server Error: {e}", 500


@voicehub.route("/chat", methods=["POST", "GET"])
@login_required
def chat_page():
    chat_id = request.args.get("chat_id", type=str)
    if not chat_id:
        return "Chat ID is required", 400

    try:
        chat = (
            db_ses.query(ChatsOfUsers).filter_by(chat_id=UUID(chat_id)).first()
        )
        if not chat:
            return redirect("/")
        list_of_users_chats = (
            db_ses.query(ChatsOfUsers).filter_by(user_id=current_user.id).all()
        )
        return render_template(
            "chat.html",
            chat=chat,
            user=current_user,
            list_of_users_chats=list_of_users_chats,
        )
    except ValueError:
        return "Invalid UUID format", 400
    except sqlalchemy.exc.SQLAlchemyError as e:
        return f"SQLAlchemy Error: {e}", 500
    except Exception as e:
        return f"Internal Server Error: {e}", 500


@voicehub.route("/delete-chat", methods=["POST", "GET"])
@login_required
def delete_chat():
    chat_id = request.args.get("chat_id")
    if chat_id:
        chat = (
            db_ses.query(ChatsOfUsers).filter_by(chat_id=UUID(chat_id)).first()
        )
        if chat:
            db_ses.delete(chat)
            db_ses.commit()

    referer = request.headers.get("Referer")
    if referer:
        return redirect(referer)
    else:
        return redirect(url_for("index"))
