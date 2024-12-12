import json

import numpy as np
import plotly.graph_objects as go

# Чтение данных из JSON файла
with open("metrics/jsons/russian_language_metrics.json", "r") as f:
    data = json.load(f)

# Получаем список моделей
models = data["models"]

# Подготовка данных для графика
v2_scores = []
v3_scores = []
v3turbo_scores = []

# Извлекаем данные и вычисляем среднее по всем метрикам для каждого текста
for metric in data["metrics"]:
    v2_avg = np.mean(
        [
            metric["relative_scores"]["v2"]["grammar"],
            metric["relative_scores"]["v2"]["style"],
            metric["relative_scores"]["v2"]["meaning"],
        ]
    )
    v3_avg = np.mean(
        [
            metric["relative_scores"]["v3"]["grammar"],
            metric["relative_scores"]["v3"]["style"],
            metric["relative_scores"]["v3"]["meaning"],
        ]
    )
    v3turbo_avg = np.mean(
        [
            metric["relative_scores"]["v3-turbo"]["grammar"],
            metric["relative_scores"]["v3-turbo"]["style"],
            metric["relative_scores"]["v3-turbo"]["meaning"],
        ]
    )

    v2_scores.append(v2_avg)
    v3_scores.append(v3_avg)
    v3turbo_scores.append(v3turbo_avg)

# Вычисляем средние значения по всем текстам
avg_scores = [np.mean(v2_scores), np.mean(v3_scores), np.mean(v3turbo_scores)]

# Создание столбчатой диаграммы
fig = go.Figure()

# Добавление столбцов
fig.add_trace(
    go.Bar(
        x=models,
        y=avg_scores,
        marker_color=["#2a76cb", "#4501cb", "#69c2f3"],
        text=[f"{v:.3f}" for v in avg_scores],
        textposition="auto",
        textfont=dict(color="white", size=20),
    )
)

# Настройка макета
fig.update_layout(
    plot_bgcolor="rgb(24, 26, 31)",
    paper_bgcolor="rgb(24, 26, 31)",
    font=dict(color="white", size=16),
    title="Средние метрики по моделям voice2text openai-whisper",
    yaxis=dict(
        title="Оценка агента (грамматика, стиль, смысл)",
        titlefont=dict(size=19),
        range=[0, 1.01],
        dtick=0.125,
    ),
    width=1200,
    height=600,
)

# Сохранение графика в файл
fig.write_html("./metrics/russian_agent_metrics.html")

print("График сохранен как 'russian_agent_metrics.html'")
