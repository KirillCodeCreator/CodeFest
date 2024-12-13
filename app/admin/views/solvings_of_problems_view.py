from .base_view import BaseView


class SolvingsOfProblemsView(BaseView):
    column_list = ("id", "key_words", "solving_of_problem")
    column_filters = ("key_words",)
    column_labels = {
        "id": "ID",
        "key_words": "Ключевые слова",
        "solving_of_problem": "Решение проблемы",
    }
    column_searchable_list = ("key_words",)
