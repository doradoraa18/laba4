import os
import random

import telebot
from dotenv import load_dotenv

from exceptions import search_image, random_image, popular_image, ApiError

# загружаем .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

# user_id -> сколько фото отправлено
photo_counter: dict[int, int] = {}


def inc_photo_counter(user_id: int) -> None:
    photo_counter[user_id] = photo_counter.get(user_id, 0) + 1


# темы для популярных картинок
POPULAR_TOPICS = [
    "nature",
    "city",
    "technology",
    "art",
    "travel",
    "people",
]


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Привет! Я бот, который ищет фотографии по ключевым словам.\n\n"
        "Команды:\n"
        "/photo <запрос> — найти фото по запросу\n"
        "/random — случайная картинка\n"
        "/popular — популярная картинка по случайной теме\n"
        "/stats — статистика отправленных тебе картинок\n\n"
        "Также можно просто написать текст, и я попробую найти картинку 🙂",
    )


@bot.message_handler(commands=["photo"])
def send_photo_by_query(message):
    try:
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            bot.reply_to(
                message,
                "Напиши запрос после команды.\nПример: /photo mountains at night",
            )
            return

        query = parts[1].strip()
        bot.send_chat_action(message.chat.id, "upload_photo")
        image_bytes = search_image(query)

        if image_bytes is None:
            bot.reply_to(
                message,
                f"Не нашёл изображений по запросу: «{query}».\n"
                "Попробуй сформулировать по‑другому (лучше на английском).",
            )
            return

        inc_photo_counter(message.from_user.id)
        bot.send_photo(
            message.chat.id,
            image_bytes,
            caption=f"Вот что нашлось по запросу: «{query}»",
        )
    except ApiError as e:
        bot.reply_to(message, f"Ошибка при обращении к API: {e}")
    except Exception:
        bot.reply_to(message, "Произошла непредвиденная ошибка при поиске изображения.")


@bot.message_handler(commands=["random"])
def send_random_photo(message):
    try:
        bot.send_chat_action(message.chat.id, "upload_photo")
        image_bytes = random_image()

        if image_bytes is None:
            bot.reply_to(
                message,
                "Не удалось получить случайное изображение, попробуй позже.",
            )
            return

        inc_photo_counter(message.from_user.id)
        bot.send_photo(
            message.chat.id,
            image_bytes,
            caption="Случайное изображение ✨",
        )
    except ApiError as e:
        bot.reply_to(message, f"Ошибка при обращении к API: {e}")
    except Exception:
        bot.reply_to(message, "Произошла непредвиденная ошибка при отправке изображения.")


@bot.message_handler(commands=["popular"])
def send_popular_photo(message):
    try:
        topic = random.choice(POPULAR_TOPICS)
        bot.send_chat_action(message.chat.id, "upload_photo")
        image_bytes = popular_image(topic)

        if image_bytes is None:
            bot.reply_to(
                message,
                "Не удалось получить популярное изображение, попробуй позже.",
            )
            return

        inc_photo_counter(message.from_user.id)
        bot.send_photo(
            message.chat.id,
            image_bytes,
            caption=f"Популярная тема: «{topic}»",
        )
    except ApiError as e:
        bot.reply_to(message, f"Ошибка при обращении к API: {e}")
    except Exception:
        bot.reply_to(message, "Произошла непредвиденная ошибка при отправке изображения.")


@bot.message_handler(commands=["stats"])
def send_stats(message):
    try:
        count = photo_counter.get(message.from_user.id, 0)
        bot.reply_to(message, f"Тебе уже отправлено {count} фотографий 🖼️")
    except Exception:
        bot.reply_to(message, "Не удалось показать статистику, попробуй позже.")


@bot.message_handler(content_types=["text"])
def handle_text(message):
    try:
        text = message.text.strip()

        # неизвестные команды
        if text.startswith("/"):
            bot.reply_to(
                message,
                "Я не знаю такую команду.\n"
                "Доступные: /photo, /random, /popular, /stats.\n"
                "Или просто напиши текст, и я попробую найти картинку 🙂",
            )
            return

        # обычный текст — считаем поисковым запросом
        bot.send_chat_action(message.chat.id, "upload_photo")
        image_bytes = search_image(text)

        if image_bytes is None:
            bot.reply_to(
                message,
                f"Не нашёл изображений по запросу: «{text}».\n"
                "Попробуй переформулировать запрос (лучше на английском).",
            )
            return

        inc_photo_counter(message.from_user.id)
        bot.send_photo(
            message.chat.id,
            image_bytes,
            caption=f"Вот что нашлось по запросу: «{text}»",
        )
    except ApiError as e:
        bot.reply_to(message, f"Ошибка при обращении к API: {e}")
    except Exception:
        bot.reply_to(message, "Произошла непредвиденная ошибка при обработке сообщения.")


if __name__ == "__main__":
    print("Image search bot started")
    bot.infinity_polling()
