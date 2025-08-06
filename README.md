# VK Sentiment Analysis Bot 🤖📊

Этот Telegram-бот позволяет пользователю выбрать группу ВКонтакте и провести анализ тональности комментариев к постам с определённым ключевым словом.

## 📌 Возможности

- Выбор одной из популярных VK-групп (RT или РИА Новости)
- Выбор ключевого слова для поиска постов
- Получение последних постов по ключевому слову
- Сбор комментариев к каждому посту
- Перевод комментариев на английский язык с помощью Google Translator
- Анализ тональности (VADER sentiment analysis)
- Сохранение результатов в CSV-файл
- Ответ пользователю с результатами в Telegram

## 🛠️ Технологии и библиотеки

- Python 3.10+
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [deep-translator](https://github.com/nidhaloff/deep-translator)
- NLTK (VADER Sentiment Analyzer)
- VK API
- CSV, datetime, requests

## ⚙️ Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/yourname/vk-sentiment-bot.git
cd vk-sentiment-bot
```

2. Установите зависимости:

```bash
uv sync
```

3. Убедитесь, что вы скачали VADER лексикон (автоматически подгружается):

```python
import nltk
nltk.download('vader_lexicon')
```

## 🔑 Настройки

- Замените `TELEGRAM_BOT_TOKEN` в `main.py` на ваш токен Telegram-бота.
- Убедитесь, что в `posts_in_group()` и `comments_in_post()` указан актуальный `access_token` VK (создаётся через VK API).

## 🚀 Запуск

```bash
python main.py
```

После запуска:

- В Telegram отправьте команду `/start`
- Выберите группу VK
- Выберите слово для анализа
- Получите отчёт о среднем значении тональности комментариев под соответствующими постами

## 📁 Выходной файл

Все результаты сохраняются в файл `file.csv` в формате:

```csv
Текст поста, Средняя тональность, Дата поста
```
Круговые диаграммы можно посмотреть, запустив файл diagrams.py

## ⚠️ Важно

- Используемый VK access token должен обладать правами на доступ к API.
- Анализ проводится только для первых 100 комментариев каждого поста (ограничение API).
