"""Главный модуль проекта."""

from flask import Flask, redirect, render_template, url_for
from flask_admin import Admin, AdminIndexView
from flask_babel import Babel
from flask_login import LoginManager

from app.admin.localization.admin_localization import get_locale
from app.admin.views.solvings_of_problems_view import SolvingsOfProblemsView
from app.admin.views.treatments_of_users_view import TreatmentsOfUsersView
from app.admin.views.users_view import UsersView
from app.config import config
from app.models import db_session
from app.models.solvings_of_problems import SolvingsOfProblems
from app.models.treatments_of_users import TreatmentsOfUsers
from app.models.users import Users
from app.voicehub.routes import voicehub


def create_app() -> Flask:
    """Создает сессию Flask

    Returns:
        Flask: app с названием __name__ и классом Flask
    """
    app = Flask(
        __name__,
        template_folder="../src/public/html",
        static_folder="../src/public/styles",
    )
    app.config.from_object(config)
    db_session.global_init(config.DATABASE_URI)
    db_ses = db_session.create_session()
    admin_panel = Admin(
        app,
        name="VoiceHub Admin",
        index_view=AdminIndexView(
            name="VoiceHub Admin",
            url="/admin",
        ),
        template_mode=app.config["ADMIN_TEMPLATE_MODE"],
    )
    admin_panel.add_views(
        UsersView(
            Users,
            db_ses,
            name="Пользователи",
        ),
        SolvingsOfProblemsView(
            SolvingsOfProblems,
            db_ses,
            name="Решения проблем",
        ),
        TreatmentsOfUsersView(
            TreatmentsOfUsers,
            db_ses,
            name="Обращения пользователей",
        ),
    )
    login_manager = LoginManager()
    login_manager.init_app(app)
    babel = Babel(  # noqa
        app,
        locale_selector=get_locale,
    )
    app.register_blueprint(
        voicehub,
    )

    @login_manager.user_loader
    def load_user(user_id):
        """Загрузка юзера"""
        return db_ses.query(Users).get(user_id)

    @app.route("/not-found")
    def not_found():
        """Страница для ненайденных страниц"""
        return (
            render_template("404.html"),
            404,
        )

    @app.errorhandler(404)
    def custom_404(error):
        """Кастомный обработчик 404 ошибки"""
        return redirect(url_for("not_found"))

    @app.errorhandler(401)
    def custom_401(error):
        """Кастомный обработчик 401 ошибки"""
        return redirect("/login")

    return app
