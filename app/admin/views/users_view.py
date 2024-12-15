from .base_view import BaseView


class UsersView(BaseView):
    """Вьюха юзеров"""

    can_create = False
    column_list = (
        "id",
        "name",
        "email",
        "admin",
    )
    column_filters = ("name", "email", "admin")
    column_labels = {
        "id": "ID",
        "name": "Имя",
        "email": "Почта",
        "admin": "Админ",
    }
    column_editable_list = (
        "name",
        "email",
        "admin",
    )
    column_searchable_list = ("name", "email")
