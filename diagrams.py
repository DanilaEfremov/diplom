import pandas as pd
import matplotlib.pyplot as plt

file_path = 'file_parade.csv'
df = pd.read_csv(file_path)

sentiment_scores = df.iloc[:, 1]

def classify_sentiment(score):
    """
    Классифицирует числовой показатель тональности в категорию.

    :param score : float
        Числовое значение тональности (например, результат анализа текста).

    :return: str
        Категория тональности:
        - 'Позитивное' при score >= 0.05
        - 'Негативное' при score <= -0.05
        - 'Нейтральное' в остальных случаях
    """
    if score >= 0.05:
        return 'Позитивное'
    elif score <= -0.05:
        return 'Негативное'
    else:
        return 'Нейтральное'

# Применение классификации
sentiment_labels = sentiment_scores.apply(classify_sentiment)

# Подсчёт количества каждого типа
sentiment_counts = sentiment_labels.value_counts()

# Фиксированный порядок и цвета
sentiment_order = ['Позитивное', 'Нейтральное', 'Негативное']
sentiment_colors = {
    'Позитивное': '#00cc00',   # ярко-зелёный
    'Нейтральное': '#ffcc00',  # ярко-жёлтый
    'Негативное': '#cc0000'    # ярко-красный
}

sentiment_counts = sentiment_counts.reindex(sentiment_order, fill_value=0)

# Визуализация
plt.figure(figsize=(6, 6))
plt.pie(
    sentiment_counts,
    labels=sentiment_counts.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=[sentiment_colors[label] for label in sentiment_counts.index]
)
plt.title('Распределение новостей по настроению')
plt.axis('equal')
plt.tight_layout()
plt.show()