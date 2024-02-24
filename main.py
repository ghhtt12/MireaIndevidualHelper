import telebot
from telebot import types  # для указание типов
import config

bot = telebot.TeleBot(config.token)
#fjv
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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Вывести Расписание")
        btn2 = types.KeyboardButton("Узнать о дедлайнах")
        btn3 = types.KeyboardButton("Поставить новый дедлайн")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2,btn3,back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)

    elif (message.text == "Вывести Расписание"):
        bot.send_message(message.chat.id, text="Расписание")

    elif (message.text == "Узнать о дедлайнах"):
        bot.send_message(message.chat.id, text="Дедлайны")

    elif (message.text == "Поставить новый дедлайн"):
        bot.send_message(message.chat.id, text="Новый дедлайн")

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
        markup.add(button1, button2,btn3)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)

    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")


bot.polling(none_stop=True)
