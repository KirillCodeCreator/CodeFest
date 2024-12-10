from flask import Flask, redirect, render_template, url_for
from flask_admin import Admin, AdminIndexView
from flask_babel import Babel
from flask_login import LoginManager

from app.admin.localization.admin_localization import get_locale
from app.admin.views.notifications_views import NotificationsView
from app.admin.views.users_view import UsersView
from app.config import config
from app.models import db_session
from app.models.notifications import Notifications
from app.models.users import Users


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db_session.global_init(config.DATABASE_URI)
    db_ses = db_session.create_session()
    admin_panel = Admin(
        app,
        name="BookSlice Admin",
        index_view=AdminIndexView(
            name="BookSlice Admin",
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
        NotificationsView(
            Notifications,
            db_ses,
            name="Уведомления",
        ),
    )
    login_manager = LoginManager()
    login_manager.init_app(app)
    babel = Babel(  # noqa
        app,
        locale_selector=get_locale,
    )

    @login_manager.user_loader
    def load_user(user_id):
        """Загрузка юзера"""
        return db_ses.query(Users).get(user_id)

    @app.route("/unauthorized")
    def unauthorized():
        """Страница для неавторизованных пользователей"""
        return (
            render_template("./errors/unauth.html", title="Войдите в аккаунт"),
            401,
        )

    @app.route("/not-found")
    def not_found():
        """Страница для ненайденных страниц"""
        return (
            render_template("./errors/404.html", title="404 Not Found"),
            404,
        )

    # Обработчик ошибки 404
    @app.errorhandler(404)
    def custom_404(error):
        """Кастомный обработчик 404 ошибки"""
        return redirect(url_for("not_found"))

    # Обработчик ошибки 401
    @app.errorhandler(401)
    def custom_401(error):
        """Кастомный обработчик 401 ошибки"""
        return redirect(url_for("unauthorized"))

    return app
