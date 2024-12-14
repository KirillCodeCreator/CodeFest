import json

from dotenv import dotenv_values
from mistralai import Mistral

from app.voicehub.functions.extract_keywords import extract_keywords_with_llm


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
    return json.loads(response.choices[0].message.content)


print(
    make_treatment_of_user(
        1,
        """Пользователь столкнулся с трудностями при попытке создать новый чат с конкретным человеком в приложении для
    обмена сообщениями. Несмотря на многочисленные попытки, пользователь не может найти нужную опцию или выполнить
    необходимые шаги для начала нового чата.""",
    )
)
