import json

import numpy as np
import plotly.graph_objects as go

# Чтение данных из JSON файла
with open("metrics/jsons/models_metrics.json", "r") as f:
    data = json.load(f)

# Получаем список моделей
models = data["model"]

# Подготовка данных для графика
v2_scores = []
v3_scores = []
v3turbo_scores = []

# Извлекаем данные из структуры JSON
for metric in data["metrics"]:
    v2_scores.append(metric["relative_quality"]["v2"])
    v3_scores.append(metric["relative_quality"]["v3"])
    v3turbo_scores.append(metric["relative_quality"]["v3-turbo"])

# Вычисляем средние значения
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
        title="Среднее относительное качество по оценке агента",
        titlefont=dict(size=19),
        range=[0, 1.01],
        dtick=0.125,
    ),
    width=1200,
    height=600,
)

# Сохранение графика в файл
fig.write_html("./metrics/agent_metrics.html")

print("График сохранен как 'agent_metrics.html'")
