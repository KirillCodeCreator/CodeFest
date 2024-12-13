from app.voicehub.functions.extract_keywords import extract_keywords_with_llm


def make_treatment_of_user(user_id: int, treatment: str):
    json_example = """
    {
        "description": "Описание заявки",
        "key_words": "Ключевые слова",
        "data_of_treatment": "Заявка",
        "user_id": 1,
    }
    """
    extract_keywords_with_llm(treatment)
    pass


make_treatment_of_user(1, "test")
