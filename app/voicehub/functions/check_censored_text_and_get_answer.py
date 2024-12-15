import time

from dotenv import dotenv_values
from mistralai import Mistral


def check_censored_text_function(text: str) -> str:
    prompt = f"""Привет! Ты ИИ-ответчик на приятные пожелания пользователя, который написал отзыв.
    Твоя задача ответить одним предложением на отзыв что-то на подобие "Спасибо большое! ..."
    Текст:
    {text}
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
        temperature=0.2,
    )
    time.sleep(1)
    return response.choices[0].message.content


# print(
#     check_censored_text_function(
#         text="Спасибо за отличный сервис! Я очень доволен покупкой."
#     )
# )
# print(
#     check_censored_text_function(
#         text="Ваш продукт отстой! Я требую вернуть деньги, или я вас всех убью!"
#     )
# )
