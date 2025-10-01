import telebot
from telebot import types

# 🔑 Токен твоего бота
TOKEN = "7250322731:AAHaHXE1YWslI_7sCKAQbb2TCG6u843iwM8"
bot = telebot.TeleBot(TOKEN)

# 🆔 Айди админа
ADMIN_ID = 7278760867

# Словарь для отслеживания пользователей
waiting_for_message = {}


# --- Стартовая команда ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("📋 Отправить анкету", callback_data="write_and_forward")
    markup.add(btn)

    # Отправляем фото с кнопкой
    with open("hueta.jpg", "rb") as photo:
        bot.send_photo(
            message.chat.id,
            photo=photo,
            caption="Показать, что я умею?\n\nНажми кнопку и пришли свою анкету одним сообщением 👇",
            reply_markup=markup
        )


# --- Обработка кнопки ---
@bot.callback_query_handler(func=lambda call: call.data == "write_and_forward")
def process_button(call):
    waiting_for_message[call.from_user.id] = True
    bot.send_message(call.message.chat.id, "✍ Мы готовы принять твою анкету.\n\nПожалуйста, отправь её одним сообщением.")


# --- Пересылка сообщения админу ---
@bot.message_handler(func=lambda message: message.from_user.id in waiting_for_message)
def forward_message(message):
    bot.send_message(
        ADMIN_ID,
        f"📩 Вам пришла новая анкета от @{message.from_user.username or message.from_user.id}:"
    )
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)

    bot.send_message(
        message.chat.id,
        "✅ Ваша анкета успешно отправлена администратору. Спасибо за активность!"
    )

    # Сбрасываем состояние
    del waiting_for_message[message.from_user.id]


# --- Запуск ---
print("Бот запущен...")
bot.polling(none_stop=True)