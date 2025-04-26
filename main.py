"""!
@mainpage Телеграм-бот помощник студента

@section overview Обзор
Этот бот предназначен для помощи студентам в организации учебного процесса. 
Он предоставляет следующие возможности:
- Просмотр расписания занятий
- Установка напоминаний о дедлайнах
- Получение информации о текущих дедлайнах

@section usage Использование
Основные команды бота:
- /start - начать работу с ботом
- /reminder - установить новое напоминание

@author koval_0618
@date 2025
"""

import telebot
from telebot import types
import config
from rasp import pr1, pr
import datetime
import threading

bot = telebot.TeleBot(config.token)
dict1 = {}


def remnder():
    """!
    @brief Функция для работы с напоминаниями

    Содержит вложенные функции для обработки команды /reminder:
    - reminder_message - обработчик команды
    - set_reminder_name - установка названия напоминания
    - reminder_set - установка времени напоминания
    - send_reminder - отправка напоминания пользователю
    """

    @bot.message_handler(commands=['reminder'])
    def reminder_message(message):
        """!
        @brief Обработчик команды /reminder

        Запрашивает у пользователя название напоминания.
        @param message Объект сообщения от пользователя
        """
        bot.send_message(message.chat.id, 'Введите название напоминания:')
        bot.register_next_step_handler(message, set_reminder_name)

    def set_reminder_name(message):
        """!
        @brief Установка названия напоминания

        Сохраняет название напоминания и запрашивает дату и время.
        @param message Объект сообщения от пользователя
        """
        user_data = {}
        user_data[message.chat.id] = {'reminder_name': message.text}
        bot.send_message(message.chat.id,
                         'Введите дату и время, когда вы хотите получить напоминание в формате ГГГГ-ММ-ДД чч:мм:сс.')
        bot.register_next_step_handler(message, reminder_set, user_data)

    def reminder_set(message, user_data):
        """!
        @brief Установка времени напоминания

        Проверяет корректность введенной даты и устанавливает таймер.
        @param message Объект сообщения от пользователя
        @param user_data Данные пользователя (название напоминания)
        """
        try:
            reminder_time = datetime.datetime.strptime(message.text, '%Y-%m-%d %H:%M:%S')
            now = datetime.datetime.now()
            delta = reminder_time - now

            if delta.total_seconds() <= 0:
                bot.send_message(message.chat.id, 'Вы ввели прошедшую дату, попробуйте еще раз.')
            else:
                reminder_name = user_data[message.chat.id]['reminder_name']
                dict1[reminder_name] = reminder_time
                bot.send_message(message.chat.id,
                                 'Напоминание "{}" установлено на {}.'.format(reminder_name, reminder_time))
                reminder_timer = threading.Timer(delta.total_seconds(), send_reminder, [message.chat.id, reminder_name])
                reminder_timer.start()

        except ValueError:
            bot.send_message(message.chat.id, 'Вы ввели неверный формат даты и времени, попробуйте еще раз.')

    def send_reminder(chat_id, reminder_name):
        """!
        @brief Отправка напоминания пользователю

        @param chat_id ID чата с пользователем
        @param reminder_name Название напоминания
        """
        bot.send_message(chat_id, 'Время получить ваше напоминание "{}"!'.format(reminder_name))


remnder()


@bot.message_handler(commands=['start'])
def start(message):
    """!
    @brief Обработчик команды /start

    Создает главное меню бота с кнопками.
    @param message Объект сообщения от пользователя
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    btn2 = types.KeyboardButton("❓ Задать вопрос")
    btn3 = types.KeyboardButton("👨‍🎓 Помощь студенту")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я индивидуальный помощник студента".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    """!
    @brief Основной обработчик текстовых сообщений

    Обрабатывает все текстовые сообщения и кнопки меню.
    @param message Объект сообщения от пользователя
    """
    if (message.text == "👋 Поздороваться"):
        bot.send_message(message.chat.id, text="Привеет,спасибо что используешь нашего бота!)")

    elif (message.text == "👨‍🎓 Помощь студенту"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Вывести Расписание")
        btn2 = types.KeyboardButton("Узнать о дедлайнах")
        btn3 = types.KeyboardButton("Поставить новый дедлайн")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)

    elif (message.text == "Вывести Расписание"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn12 = types.KeyboardButton("ИВБО-01-22")
        btn22 = types.KeyboardButton("ИВБО-04-22")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn12, btn22, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)

    elif (message.text == "ИВБО-01-22"):
        bot.send_message(message.chat.id, text=pr1('ИВБО-01-22'))

    elif (message.text == "ИВБО-04-22"):
        bot.send_message(message.chat.id, text=pr1('ИВБО-04-22'))

    elif (message.text == "Узнать о дедлайнах"):
        bot.send_message(message.chat.id, text=str(pr(dict1)))

    elif (message.text == "Поставить новый дедлайн"):
        bot.send_message(message.chat.id, text="/reminder")

    elif (message.text == "❓ Задать вопрос"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как меня зовут?")
        btn2 = types.KeyboardButton("Что я могу?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)

    elif (message.text == "Как меня зовут?"):
        bot.send_message(message.chat.id, "MireaIndevidualHelper")

    elif message.text == "Что я могу?":
        bot.send_message(message.chat.id, text="Помочь вам эффективно распарядиться вашим временем")

    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("👋 Поздороваться")
        button2 = types.KeyboardButton("❓ Задать вопрос")
        btn3 = types.KeyboardButton("👨‍🎓 Помощь студенту")
        markup.add(button1, button2, btn3)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)

    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")


bot.polling(none_stop=True)