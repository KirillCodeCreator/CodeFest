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
    Извлекает оригинальный текст и тексты всех моделей.

    Args:
        text_name: Название текста
        models: Список названий моделей

    Returns:
        Кортеж из оригинального текста и списка текстов моделей
    """
    original_path = f"metrics/data_sets/originals/{text_name}.txt"

    try:
        with open(original_path, "r", encoding="utf-8") as file:
            original_text = file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Не найден оригинальный файл: {original_path}"
        )

    generated_texts = []
    for model in models:
        generated_path = (
            f"metrics/data_sets/voice_2_text/{model}/{text_name}.txt"
        )
        try:
            with open(generated_path, "r", encoding="utf-8") as file:
                generated_texts.append(file.read().strip())
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Не найден сгенерированный файл: {generated_path}"
            )

    return original_text, generated_texts


def main():
    api_key = dotenv_values("./.env")["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)
    models = ["v2", "v3", "v3-turbo"]  # список моделей для сравнения

    json_example = """
    {
        "text-name": "cooking",
        "relative_scores": {
            "v2": {
                "grammar": 0.00,
                "style": 0.00,
                "meaning": 0.00
            },
            "v3": {
                "grammar": 0.00,
                "style": 0.00,
                "meaning": 0.00
            },
            "v3-turbo": {
                "grammar": 0.00,
                "style": 0.00,
                "meaning": 0.00
            }
        }
    }
    """

    # Получаем список всех текстов
    text_names = get_all_text_names()

    # Загружаем существующие метрики
    try:
        with open("metrics/jsons/russian_language_metrics.json", "r") as file:
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
            original_text, generated_texts = get_texts_from_directories(
                text_name, models
            )

            time.sleep(1.5)

            models_text = "\n".join(
                [
                    f"Текст модели {model}: {text}"
                    for model, text in zip(models, generated_texts)
                ]
            )

            prompt_to_llm = f"""Ты эксперт по русскому языку. Сравни качество
            расшифровки текста разными моделями.
            Оценивать нужно объективно и относительно друг друга.
            Мне это нужно для построения графиков метрик.

            Оцени каждую модель по следующим параметрам (от 0 до 1, шаг 0.01):
            - grammar: относительное качество грамматики, пунктуации и
            орфографии
            - style: относительное качество сохранения стиля и регистра речи
            - meaning: относительное качество сохранения исходного смысла

            Оригинальный текст: {original_text}

            {models_text}

            Верни результат только в формате JSON:
            {json_example}

            text-name должен быть: {text_name}"""

            response = client.chat.complete(
                model="mistral-large-latest",
                messages=[
                    {
                        "role": "user",
                        "content": prompt_to_llm,
                    }
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
            if "rate limit" in str(e).lower():
                print("Превышен лимит запросов, ожидание 60 секунд...")
                time.sleep(60)
            continue

    # Сохраняем все метрики с информацией о моделях
    metrics_data = {"models": models, "metrics": existing_metrics}

    with open("metrics/jsons/russian_language_metrics.json", "w") as file:
        json.dump(metrics_data, file, indent=4, ensure_ascii=False)

    print("Все метрики успешно сохранены.")


if __name__ == "__main__":
    main()
