import json
import time

from dotenv import dotenv_values
from mistralai import Mistral


def find_best_solve_of_problem(problem: str, solvings: list[str]) -> str:
    """
    Функция find_best_solve_of_problem принимает описание проблемы и список предложенных решений и возвращает самое
    логичное решение.

    :param problem: Описание проблемы
    :type problem: str
    :param solvings: Список предложенных решений
    :type solvings: list[str]
    :return: Самое логичное решение
    :rtype: str
    """
    json_example = """
    Есть решение проблемы: {"solving": "Решение проблемы"}
    Нет решения: {"solving": "Ваше обращение сохранено, мы перезвоним Вам позже!"}
    """
    prompt = f"""Вы - работник техподдержки. Ваша задача — проанализировать предоставленные решения проблем и выбрать
    самое логичное решение для
    данной проблемы. Важно, чтобы вы не придумывали ничего нового, а основывались только на предоставленных данных.
    Описание проблемы:
    {problem}
    Предоставленные решения:
    {solvings}
    Инструкции:

    1 Выберите одно решение, которое наиболее логично и эффективно решает проблему.
    2 Пример ответа:
    {json_example}
    Примечание:
    Не придумывайте новых решений. Используйте только предоставленные решения и данные."""
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
    return json.loads(response.choices[0].message.content)["solving"]


# print(
#     find_best_solve_of_problem(
#         problem="Мой интернет не работает.",
#         solvings=[
#             "Проверьте, подключен ли кабель интернета.",
#             "Перезагрузите роутер.",
#             "Обратитесь к провайдеру.",
#         ],
#     )
# )
# print(
#     find_best_solve_of_problem(
#         problem="Мой компьютер не включается.",
#         solvings=[
#             "Проверьте, подключен ли кабель питания.",
#             "Перезагрузите компьютер.",
#             "Обратитесь в сервисный центр.",
#         ],
#     )
# )
