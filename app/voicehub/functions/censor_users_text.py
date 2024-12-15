import json

from dotenv import dotenv_values
from mistralai import Mistral


def censor_users_text_function(text: str) -> dict:
    """Цензура текста, который юзер передает в голосовом сообщении

    Args:
        text (str): Текст гс

    Returns:
        dict: Цензурованный текст
    """
    json_example = """
    {
        "complaint": "True",
        "text": "Цензурованный текст пользователя"
    }
    """
    prompt = f"""Ты - цензор текста. Проверь, является ли предоставленный текст жалобой. Жалоба обычно включает в себя
    описание проблемы, недовольство каким-либо аспектом продукта или услуги, или просьбу о помощи в решении конкретной
    ситуации. Если текст является жалобой, отметь его как "complaint": "True".
    Если текст не является жалобой, отметь его как "complaint": "False".
    Проверь текст на наличие ненормативной лексики, оскорблений, угроз или других неприемлемых выражений.
    Если текст содержит ненормативную лексику или неприемлемые выражения, замени их на более приемлемые альтернативы
    или удали их. Если текст содержал ненормативную лексику и был
    исправлен, верни исправленный вариант текста.
    Если текст не содержал ненормативной лексики, верните оригинальный текст. Пример итогового ответа:
    {json_example}
    Текст для цензуры: {text}"""
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


# print(
#     censor_users_text_function(
#         text="Ваш продукт отстой! Я требую вернуть деньги, или я вас всех убью!"
#     )
# )
