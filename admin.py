import time
import telebot
import config
import datetime
from telebot import types

admin_bot = telebot.TeleBot(config.ADMIN_TOKEN)
second_chat_id = '627500744'


#проверка оплаты в месяц
users = {
    'Рауан Аблайхан':datetime.date(2023, 3, 31),
    'Есекеев Амиржан':datetime.date(2023, 3, 9),
    'Абай Халиков':datetime.date(2023, 3, 31)
}
def notify_user(user_id):
    user_date = users[user_id]
    days_left = (user_date - datetime.date.today()).days
    if days_left ==1:
        message =  f'Уважаемый администратор, у пользователя {user_id} завтра заканчивается месячный абонимент'

    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text='Востоновить абонимент', callback_data=user_id)
    markup.add(button)

    admin_bot.send_message(second_chat_id,message,reply_markup=markup)

@admin_bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.data

    users[user_id] = datetime.date.today() + datetime.timedelta(days=30)
    admin_bot.answer_callback_query(call.id, text= f'Абонимент пользователя {user_id} восстановлен')

for user_id, user_date in users.items():
    if user_date == datetime.date.today() + datetime.timedelta(days=1):
        notify_user(user_id)


#добавление учеников
@admin_bot.message_handler(commands=['add_user'])
def add_user(message):
    if message.chat.type == 'private':
        admin_bot.reply_to(message,'Пожалуйста, отправьте фамилия,имя пользователя, которого нужно добавить')
        admin_bot.register_next_step_handler(message, add_user_step)

def add_user_step(message):
    user_name = message.text
    users[user_name] = datetime.date.today() + datetime.timedelta(days=30)
    admin_bot.reply_to(message, f'Пользователь {user_name} успешно добавлен')


#удаление учеников
@admin_bot.message_handler(commands=['delete_user'])
def delete_user(message):
    markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
    for user_id in users:
        markup.add(types.KeyboardButton(user_id))
    markup.add(types.KeyboardButton('Отмена'))

    admin_bot.send_message(second_chat_id, 'Выберите ученика для удаление:', reply_markup=markup)
    admin_bot.register_next_step_handler(message, delete_user_confirm)

def delete_user_confirm(message):
    if message.text == 'Отмена':
        admin_bot.send_message(second_chat_id, 'Удаление отменено', reply_markup=types.ReplyKeyboardRemove())
        return
    del users[message.text]
    admin_bot.send_message(second_chat_id, 'Ученик удален', reply_markup=types.ReplyKeyboardRemove())


#список учеников
@admin_bot.message_handler(commands=['list_users'])
def list_users(message):
    users_list = "\n".join(users.keys())
    admin_bot.send_message(second_chat_id, f"Список учеников:\n{users_list}")



admin_bot.polling()
