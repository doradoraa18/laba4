import os
import random
import telebot

from exceptions import get_cat_image


BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

JOKES = [
    "Когда дедлайн завтра, а ты котик.",
    "Я не толстый, я пушистый.",
    "Если я сплю — значит, так надо.",
    "Работа? Не, я кот."
]

# user_id -> сколько котов отправлено
cat_counter = {}


def inc_counter(user_id: int) -> None:
    cat_counter[user_id] = cat_counter.get(user_id, 0) + 1


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Привет! Я бот с котиками.\n"
        "Команды: /cat — котик, /funnycat — смешной котик, /stats — статистика котиков.",
    )


@bot.message_handler(commands=["cat"])
def send_cat(message):
    try:
        image_bytes = get_cat_image()
        if image_bytes is None:
            bot.reply_to(message, "Не удалось загрузить котика, попробуй ещё раз позже.")
            return

        inc_counter(message.from_user.id)
        bot.send_photo(message.chat.id, image_bytes, caption="Котик 🐱")
    except Exception:
        bot.reply_to(message, "Произошла ошибка при отправке котика.")


@bot.message_handler(commands=["funnycat"])
def send_funny_cat(message):
    try:
        image_bytes = get_cat_image()
        if image_bytes is None:
            bot.reply_to(message, "Не удалось загрузить котика, попробуй ещё раз позже.")
            return

        inc_counter(message.from_user.id)
        caption = random.choice(JOKES)
        bot.send_photo(message.chat.id, image_bytes, caption=caption)
    except Exception:
        bot.reply_to(message, "Произошла ошибка при отправке смешного котика.")


@bot.message_handler(commands=["stats"])
def send_stats(message):
    try:
        count = cat_counter.get(message.from_user.id, 0)
        bot.reply_to(message, f"Тебе уже отправлено {count} котиков 🐱")
    except Exception:
        bot.reply_to(message, "Не удалось показать статистику, попробуй позже.")


@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    bot.reply_to(
        message,
        "иди в попуу\n"
        "Используй: /cat, /funnycat или /stats.",
    )


@bot.message_handler(content_types=["text"])
def fallback_text(message):
    if message.text.startswith("/"):
        bot.reply_to(
            message,
            "Я не знаю такую команду.\n"
            "Доступные: /cat, /funnycat, /stats.",
        )
    else:
        bot.reply_to(
            message,
            "Я понимаю только команды.\n"
            "Используй: /cat, /funnycat или /stats.",
        )


if __name__ == "__main__":
    print("Cat bot started")
    bot.infinity_polling()
