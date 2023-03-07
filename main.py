import datetime
import os
import sqlite3
import telebot
import config
import random
import time

from telebot.types import Message
from telebot import types


bot = telebot.TeleBot(config.TOKEN)
admin_bot = telebot.TeleBot(config.ADMIN_TOKEN)
base_db = telebot.TeleBot(config.basedate)


second_chat_id = '627500744'

conn = sqlite3.connect('database.db')


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('Тренерский штаб', callback_data='trainer')
    item2 = types.InlineKeyboardButton('Расписание групп', callback_data='schedule')
    item3 = types.InlineKeyboardButton('Записаться на пробное занятие', callback_data='enroll')
    item4 = types.InlineKeyboardButton('Информация', callback_data='information')
    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id, '<b>Здраствуйте, вас приветсвует Академия Бразильского Джиу Джитсу!</b>' '\n\n🥋Мы являемся профессиональной спортивной командой' '\n🧒 Тренируем детей от 4-х лет' '\n🧑 Подростковая группа' 
                                      '\n👩 Женская группа' '\n🧔 Мужская группа' '\n\n 📱Instagram: <a href="https://www.instagram.com/nomad.jj/?next=%2F">nomad.jj</a>',
    parse_mode='HTML', reply_markup=markup)




@bot.callback_query_handler(func=lambda call: call.data == 'enroll')
def enroll_handler(call):
    message_text = '<b>❗️ВАЖНО❗️</b>' + '\n <i>Заполните все поля!</i>' '\n\n 1.Напишите фамилия, имя кто собирается прийти ✉️' + '\n 2.Сколько лет?🙋🏻‍♂️' + '\n 3.На какое время собираетесь прийти ⏰' + '\n 4.Ваш номер телефона 📞' + '\n\n Можете отправить данные одним сообщением , они автоматически отправятся на базу🔐'
    bot.send_message(chat_id=call.message.chat.id, text=message_text, parse_mode='HTML')

    bot.register_next_step_handler(call.message, process_enroll)


def process_enroll(message):
     markup = types.InlineKeyboardMarkup(row_width=2)
     item1 = types.InlineKeyboardButton('Меню', callback_data='menu')
     item2 = types.InlineKeyboardButton('Повторить заявку', callback_data='enroll')
     markup.add(item1, item2)

     text = message.text

     bot.send_message(chat_id=message.chat.id, text="<b>Ваша заявка отправлена!</b>" + "\n\nЖдем вас в нашем зале 😁", parse_mode='HTML', reply_markup=markup)
     admin_bot.send_message(second_chat_id, 'Новый посетитель:' + f'\n{  text}')







@bot.callback_query_handler(func=lambda call: call.data == 'schedule')
def scgedule_hadler(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('Меню', callback_data='menu')
    markup.add(item1)

    schedule = open('nomad.jpg', 'rb')
    bot.send_photo(call.message.chat.id,schedule, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'information')
def information_handler(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('Меню', callback_data='menu')
    item2 = types.InlineKeyboardButton('2GIS', url='https://2gis.kz/astana/geo/9570784863331846/71.437711408361793,51.170765754869215')
    item3 = types.InlineKeyboardButton('Whatsapp', url='https://api.whatsapp.com/send/?phone=77059067996&text&type=phone_number&app_absent=0')
    markup.add(item1, item2, item3)
    bot.send_message(call.message.chat.id, '<b>❗️Информация❗️</b>' + '\n\nРаботаем ежедневно с понедельник по субботу 🗓' +
                                                '\nС 9:00 - 23:00 ⏰' + '\n\n Стоимость абонемента:' + '\n Мужчины: 25 000тг' + '\n Женщины: 25 000тг' +
                                                '\n Студенты: 20 000тг' + '\n Детский: 22 000тг' + '\n\n 📍Адрес: г. Астана, Жакып Омарова 10' + '\n  В цокольном этаже здания'
                                                '\n\n📲Напишите нам в WhatsApp для большей информации',
                     parse_mode='HTML', reply_markup=markup)





@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('Меню', callback_data='menu')
    item2 = types.InlineKeyboardButton('Следующий', callback_data='rama_trainer')
    markup.add(item1, item2)



    photo = open('olzhas.jpg', 'rb')
    photo_rama = open('rama.jpg', 'rb')



    if call.message:
        if call.data == 'trainer':
          bot.send_photo(call.message.chat.id, photo, '<b>Олжас Идирисов</b>' + '\n<i>Главный тренер</i>' '\n\n🎖Заслуженный Мастер Спорта по грэпплингу и по джиу-джитсу' + '\n🟤Является заслуженным обладателем коричневого пояса'
                  + '\n🏆Чемпион Азии по ADCC' + '\n🥋Опыт тренерской деятельности более 6-ти лет' + '\n📱Instagram: <a href="https://www.instagram.com/idrissov_jj/">idrissov_jj</a>'

                         , parse_mode='html', reply_markup=markup)
        elif call.data == 'rama_trainer':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('Предыдущий', callback_data='trainer')
            item2 = types.InlineKeyboardButton('Меню', callback_data='menu')
            markup.add(item1, item2)

            bot.send_photo(call.message.chat.id, photo_rama, '<b> Абдрахимов Рамазан </b>'+ '\n<i>Тренер Мужской группы</i>' '\n\n🎖Заслуженный Мастер Спорта по грэпплингу' + '\n🟣Владелец пурпурного пояса'
                           +'\n🏆Чемпион мира в Испании'+ '\n🥇Чемпион Казахстана' +'\n🥇Чемпион Азии'+ '\n📱Instagram: <a href="https://www.instagram.com/ramazan_abdrakhimov/">ramazan_abdrakhimov</a>'
                           , parse_mode='HTML',reply_markup=markup)

        elif call.data == 'menu':
                 welcome(call.message)







bot.polling(none_stop=True, interval=0)

admin_bot.polling(none_stop=True, interval=0)
