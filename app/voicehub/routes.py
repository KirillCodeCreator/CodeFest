from flask import Blueprint

from app.models import db_session

voicehub = Blueprint(
    "voicehub", __name__, template_folder="../templates/voicehub"
)
db_session.global_init("../app.db")
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
    return "Привет!"
