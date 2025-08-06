from deep_translator import GoogleTranslator
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import requests
import datetime
import csv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

VK_TOKEN = 'vk token'
TG_TOKEN = 'tg token'

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /start. Показывает пользователю выбор групп VK для анализа.

    :param update: Объект обновления Telegram.
    :param context: Контекст исполнения Telegram.
    :return: None
    """
    await update.message.reply_text("Привет! Выберите группу ВК, по которой хотите произвести анализ")
    keyboard = [
        [InlineKeyboardButton("Новости RT", callback_data="analyze:40316705")],
        [InlineKeyboardButton("Риа Новости", callback_data="analyze:15755094")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Нажмите для старта:", reply_markup=reply_markup)


# Обработчик кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
        Обработчик нажатий на inline-кнопки. Определяет выбранную группу или слово для анализа.

        :param update: Объект обновления Telegram.
        :param context: Контекст исполнения Telegram.
        :return: None
    """
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("analyze:"):
        group_id = int(data.split(":")[1])
        context.user_data["group_id"] = group_id  # сохраняем временно
        # Показываем следующий набор кнопок
        keyboard = [
            [InlineKeyboardButton("Парад", callback_data="word:парад")],
            [InlineKeyboardButton("Зеленский", callback_data="word:зеленский")],
            [InlineKeyboardButton("Переговоры", callback_data="word:переговоры")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Выберите слово для анализа:", reply_markup=reply_markup)

    elif data.startswith("word:"):
        word = data.split(":")[1]
        group_id = context.user_data.get("group_id")
        if group_id:
            await my_function(update, context, group_id, word)
        else:
            await query.edit_message_text("Ошибка: группа не выбрана.")


# Перевод и анализ тональности
def analyse_text(text):
    """Перевод текста на английский язык и анализ его тональности с помощью VADER.

        :param text: Исходный текст (комментарий).
        :return: Словарь с оценками тональности (pos, neu, neg).
    """
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        nltk.download('vader_lexicon', quiet=True)
        sia = SentimentIntensityAnalyzer()
        return sia.polarity_scores(translated)
    except Exception as e:  # noqa: F841
        return {'compound': 0}  # безопасная заглушка при ошибке


# Поиск постов ВК
def posts_in_group(id_group: int, find: str):
    """
        Получение постов из группы VK по ключевому слову.

        :param id_group: ID группы VK (отрицательное значение для публичных страниц).
        :param find: Ключевое слово для поиска в постах.
        :return: JSON-ответ API VK с найденными постами.
    """
    vk_token = VK_TOKEN
    url = 'https://api.vk.com/method/wall.search'
    data = {
        'access_token': vk_token,
        'owner_id': -id_group,
        'query': find,
        'owners_only': 1,
        'count': 100,
        'v': 5.199
    }
    response = requests.get(url, params=data)
    return response.json()


# Комментарии к посту ВК
def comments_in_post(id_group: int, id_post: str):
    """
        Получение комментариев к определённому посту VK.

        :param id_group: ID группы VK.
        :param id_post: ID поста.
        :return: JSON-ответ с комментариями к посту.
    """
    vk_token = VK_TOKEN
    url = 'https://api.vk.com/method/wall.getComments'
    data = {
        'access_token': vk_token,
        'owner_id': -id_group,
        'post_id': id_post,
        'count': 100,
        'v': 5.199
    }
    response = requests.get(url, params=data)
    return response.json()


# Основная функция анализа
async def my_function(update: Update, context: ContextTypes.DEFAULT_TYPE, group: int, word: str) -> None:
    """
        Основная функция анализа: ищет посты по ключевому слову, получает комментарии и анализирует их тональность.

        :param update: Объект обновления Telegram.
        :param context: Контекст исполнения Telegram.
        :param group: ID группы VK.
        :param word: Ключевое слово для анализа.
        :return: None
    """
    # word = 'парад'
    response = posts_in_group(group, word)
    posts = []
    csv_file_path = 'file.csv'

    for item in response.get('response', {}).get('items', []):
        posts.append((item['text'], item['id'], datetime.datetime.fromtimestamp(item['date'])))

    for post in posts:
        mean = 0
        count = 0
        comment_data = comments_in_post(group, post[1])
        for comment in comment_data.get('response', {}).get('items', []):
            one_comm = comment['text']
            score = analyse_text(one_comm)
            mean += score.get('compound', 0)
            count += 1

        if count > 0:
            mean /= count

        with open(csv_file_path, 'a', newline='') as file:
            if post[0] and count > 0:
                writer = csv.writer(file)
                writer.writerow((post[0], mean, post[2]))

        await update.callback_query.message.reply_text(f"Пост: {post[0]}\nСредний тон: {mean:.2f}")

# Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(TG_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен")
    app.run_polling()