import json
import time

from dotenv import dotenv_values
from mistralai import Mistral

from app.models.treatments_of_users import TreatmentsOfUsers


def extract_keywords_with_llm(text) -> list[str]:
    """
    Функция extract_keywords_with_llm принимает текст обращения и возвращает список ключевых слов, которые наиболее
    точно описывают суть проблемы.

    :param text: Текст обращения
    :type text: str
    :return: Список ключевых слов
    :rtype: list[str]
    """
    json_response = """
    {"keywords": ["проблема", "задача"]}
    """
    prompt = f"""
    Ваша задача — проанализировать следующее обращение и выделить из него ключевые слова, которые наиболее точно
    описывают суть проблемы. Все слова должны быть в именительном падеже. Ключевые слова должны быть представлены в
    виде списка через запятую и состоять из
    одного слова. Пример ответа: {json_response}

    Обращение: {text}

    Ключевые слова:
    """
    api_key = dotenv_values("./.env")["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
        response_format={
            "type": "json_object",
        },
    )
    time.sleep(1)
    return json.loads(response.choices[0].message.content)["keywords"]


def make_treatment_of_user(user_id: int, treatment: str) -> dict:
    json_example = """
    {
        "description": "Описание заявки",
        "key_words": "Ключевые слова",
        "data_of_treatment": "Заявка",
        "user_id": 1,
    }
    """
    key_words = extract_keywords_with_llm(treatment)
    prompt = f"""Ты генератор заявок для техподдержки. Твоя задача по полученным данным сформировать json-ответ.
    Пример ответа:
    {json_example}
    description - описание заявки для техподдержки. Максимум одно предложение.
    key_words - {key_words}
    data_of_treatment - полный текст запроса, как тебе дали
    user_id - id юзера, который обратился.
    user_id = {user_id}
    data_of_treatment = {treatment}"""
    api_key = dotenv_values("./.env")["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
        response_format={
            "type": "json_object",
        },
    )
    time.sleep(1)
    return json.loads(response.choices[0].message.content)


def add_treatment_to_data_base_function(
    db_session, treatment: str, user_id: int
) -> bool | Exception:
    try:
        treatment_dict = make_treatment_of_user(
            user_id=user_id, treatment=treatment
        )
        treatment = TreatmentsOfUsers(
            description=treatment_dict["description"],
            key_words=" ".join(treatment_dict["key_words"]),
            data_of_treatment=treatment_dict["data_of_treatment"],
            user_id=treatment_dict["user_id"],
        )
        db_session.add(treatment)
        db_session.commit()
        return True
    except Exception as e:
        return str(e)
