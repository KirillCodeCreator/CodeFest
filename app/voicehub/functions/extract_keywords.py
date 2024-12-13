import json

from dotenv import dotenv_values
from mistralai import Mistral


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

    return json.loads(response.choices[0].message.content)["keywords"]
