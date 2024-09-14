import telebot

TOKEN = '7402630769:AAFDSewUne84IIDTHCKIVwIxbZXNrpy7oHY' 
bot = telebot.TeleBot(TOKEN)

CHAT_ID = '-1002154827778' 

# Створюємо посилання-запрошення з параметром для бота
invite_link = bot.create_chat_invite_link(CHAT_ID, name='BotInvitation', creates_join_request=True).invite_link

# Обробник нових повідомлень у чаті
@bot.chat_join_request_handler()
def handle_join_request(update):
    user_id = update.from_user.id
    username = update.from_user.username

    # Відправляємо запит адміністратору
    request_message = f"Новий запит на приєднання:\nID: {user_id}\nUsername: @{username}"
    bot.send_message("893937933", request_message, reply_markup=generate_markup(update.chat.id, user_id))

# Створення кнопок для адміністратора
def generate_markup(chat_id, user_id):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Прийняти", callback_data=f"approve_{chat_id}_{user_id}"))
    markup.add(telebot.types.InlineKeyboardButton("Відхилити", callback_data=f"decline_{chat_id}_{user_id}"))
    return markup

# Обробка відповідей адміністратора
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data.split('_')
    action = data[0]
    chat_id = int(data[1])
    user_id = int(data[2])

    if action == 'approve':
        bot.approve_chat_join_request(chat_id, user_id)
        bot.send_message("893937933", f"Користувач @{call.message.from_user.username} був доданий до групи.")

    elif action == 'decline':
        bot.decline_chat_join_request(chat_id, user_id)
        bot.send_message("893937933", f"Запит користувача @{call.message.from_user.username} був відхилений.")

    # Видаляємо кнопки після відповіді
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

# Повідомляємо про створене посилання
bot.send_message("893937933",f"Посилання-запрошення: {invite_link}")

bot.polling()