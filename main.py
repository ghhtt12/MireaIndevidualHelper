import telebot
from telebot import types  # для указание типов
import config
from rasp import pr1,pr
import datetime
import threading

bot = telebot.TeleBot(config.token)
dict1={}
def remnder():
    @bot.message_handler(commands=['reminder'])
    def reminder_message(message):
        # Запрашиваем у пользователя название напоминания и дату и время напоминания
        bot.send_message(message.chat.id, 'Введите название напоминания:')
        bot.register_next_step_handler(message, set_reminder_name)


    # Функция, которую вызывает обработчик команды /reminder для установки названия напоминания
    def set_reminder_name(message):
        user_data = {}
        user_data[message.chat.id] = {'reminder_name': message.text}
        bot.send_message(message.chat.id,
                         'Введите дату и время, когда вы хотите получить напоминание в формате ГГГГ-ММ-ДД чч:мм:сс.')
        bot.register_next_step_handler(message, reminder_set, user_data)


    # Функция, которую вызывает обработчик команды /reminder для установки напоминания
    def reminder_set(message, user_data):
        try:
            # Преобразуем введенную пользователем дату и время в формат datetime
            reminder_time = datetime.datetime.strptime(message.text, '%Y-%m-%d %H:%M:%S')
            now = datetime.datetime.now()
            delta = reminder_time - now
            # Если введенная пользователем дата и время уже прошли, выводим сообщение об ошибке
            if delta.total_seconds() <= 0:
                bot.send_message(message.chat.id, 'Вы ввели прошедшую дату, попробуйте еще раз.')
            # Если пользователь ввел корректную дату и время, устанавливаем напоминание и запускаем таймер
            else:
                reminder_name = user_data[message.chat.id]['reminder_name']
                dict1[reminder_name]=reminder_time
                bot.send_message(message.chat.id,
                                 'Напоминание "{}" установлено на {}.'.format(reminder_name, reminder_time))
                reminder_timer = threading.Timer(delta.total_seconds(), send_reminder, [message.chat.id, reminder_name])
                reminder_timer.start()
        # Если пользователь ввел некорректную дату и время, выводим сообщение об ошибке
        except ValueError:
            bot.send_message(message.chat.id, 'Вы ввели неверный формат даты и времени, попробуйте еще раз.')


    # Функция, которая отправляет напоминание пользователю
    def send_reminder(chat_id, reminder_name):
        bot.send_message(chat_id, 'Время получить ваше напоминание "{}"!'.format(reminder_name))


    # Обработчик любого сообщения от пользователя

remnder()
@bot.message_handler(commands=['start'])
def start(message):
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
    if (message.text == "👋 Поздороваться"):
        bot.send_message(message.chat.id, text="Привеет,спасибо что используешь нашего бота!)")

    elif (message.text == "👨‍🎓 Помощь студенту"):
        bot.send_message(message.chat.id, text="Выбери,что именно тебе нужно")
        """
        Создание кнопок
        """
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
