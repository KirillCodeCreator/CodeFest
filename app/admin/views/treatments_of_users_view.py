from .base_view import BaseView


class TreatmentsOfUsersView(BaseView):
    """Вьюха проблем"""

    column_list = (
        "id",
        "description",
        "key_words",
        "data_of_treatment",
        "user_id",
    )
    column_filters = ("key_words",)
    column_labels = {
        "id": "ID",
        "description": "Описание",
        "key_words": "Ключевые слова",
        "data_of_treatment": "Данные",
        "user_id": "Пользователь",
    }
    column_searchable_list = ("key_words",)
