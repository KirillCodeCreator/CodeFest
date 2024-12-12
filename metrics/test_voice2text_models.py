import json
import os
import time

from dotenv import dotenv_values
from mistralai import Mistral


def get_all_text_names() -> list[str]:
    """
    Получает список всех доступных текстов из директории originals
    """
    originals_dir = "metrics/data_sets/originals"
    return [
        f.split(".")[0]
        for f in os.listdir(originals_dir)
        if f.endswith(".txt")
    ]


def get_texts_from_directories(
    text_name: str, models: list[str]
) -> tuple[str, list[str]]:
    """
    Извлекает оригинальный текст и расшифрованные тексты всех моделей.

    Args:
        text_name: Название текста
        models: Список названий моделей

    Returns:
        Кортеж из оригинального текста и списка расшифрованных текстов
    """
    original_path = f"metrics/data_sets/originals/{text_name}.txt"

    try:
        with open(original_path, "r", encoding="utf-8") as file:
            original_text = file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Не найден оригинальный файл: {original_path}"
        )

    decoded_texts = []
    for model in models:
        decoded_path = (
            f"metrics/data_sets/voice_2_text/{model}/{text_name}.txt"
        )
        try:
            with open(decoded_path, "r", encoding="utf-8") as file:
                decoded_texts.append(file.read().strip())
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Не найден расшифрованный файл: {decoded_path}"
            )

    return original_text, decoded_texts


def main():
    api_key = dotenv_values("./.env")["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)
    models = ["v2", "v3", "v3-turbo"]

    json_example = """
    {
        "text-name": "cooking",
        "relative_quality": {
            "v2": 0.00,
            "v3": 0.00,
            "v3-turbo": 0.00
        }
    }
    """

    # Получаем список всех текстов
    text_names = get_all_text_names()

    # Загружаем существующие метрики
    try:
        with open("metrics/jsons/models_metrics.json", "r") as file:
            data = json.load(file)
            if isinstance(data, dict):
                existing_metrics = data.get("metrics", [])
            else:
                existing_metrics = []
    except (json.JSONDecodeError, FileNotFoundError):
        existing_metrics = []

    # Обрабатываем каждый текст
    for text_name in text_names:
        try:
            original_text, decoded_texts = get_texts_from_directories(
                text_name, models
            )

            # Увеличиваем задержку до 3 секунд
            time.sleep(1.5)  # Задержка 3 секунды между запросами

            prompt_to_llm = f"""Привет! Ты краудсорсер, который сравнивает
            качество расшифровки текста тремя моделями.
            Оценивать нужно объективно. Мне это нужно для построения графиков
            метрик.

            Твоя задача прислать JSON в формате: {json_example}

            Оригинал: {original_text}

            Расшифровка модели v2: {decoded_texts[0]}
            Расшифровка модели v3: {decoded_texts[1]}
            Расшифровка модели v3-turbo: {decoded_texts[2]}

            relative_quality - относительное качество каждой модели по
            сравнению с другими (0 до 1, шаг 0.01)
            text-name - название текста ({text_name})"""

            response = client.chat.complete(
                model="mistral-large-latest",
                messages=[
                    {
                        "role": "user",
                        "content": prompt_to_llm,
                    },
                ],
                temperature=0,
                response_format={
                    "type": "json_object",
                },
            )

            new_metrics = response.choices[0].message.content
            new_metrics_dict = json.loads(new_metrics)
            existing_metrics.append(new_metrics_dict)
            print(f"Обработан текст: {text_name}")

        except Exception as e:
            print(f"Ошибка при обработке текста {text_name}: {str(e)}")
            # Если получили ошибку Rate Limit, делаем более длительную паузу
            if "rate limit" in str(e).lower():
                print("Превышен лимит запросов, ожидание 60 секунд...")
                time.sleep(60)
            continue

    # Сохраняем все метрики с информацией о модели
    metrics_data = {"model": models, "metrics": existing_metrics}

    with open("metrics/jsons/models_metrics.json", "w") as file:
        json.dump(metrics_data, file, indent=4, ensure_ascii=False)

    print("Все метрики успешно сохранены.")


if __name__ == "__main__":
    main()
