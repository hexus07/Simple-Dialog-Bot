import telebot 
import pyowm #Погода
import time #Время
from telebot import types
from pyowm.exceptions import api_response_error
import apiai, json


weather_token='f0d533caf440f9d7604e8da15f7abc76'

tele_token="809144623:AAFx-7iltSMXrNwNbgIQcqxTsT4WWVtTZPs"
start = 0

bot = telebot.TeleBot(tele_token)#TELEGRAM BOT TOKEN

owm = pyowm.OWM(weather_token, language= "ru")#WEATER



@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,"""Привет 😎
    -----Это Разговорный БОТ погоды----- 
    Если тебе скучноюю
    Просто напиши мне.....🙃
    """)
    time.sleep(2)
    bot.send_message(message.chat.id, "И кстати я знаю как тебя зовут"+"\n"+message.from_user.first_name+", не так ли?"+"\n"+"Впрочем кем бы ты не был, ты красавчик!🤗")
@bot.message_handler(commands=['help'])
def help_me(message):
    bot.send_message(message.chat.id,"""Список команд:
    /start - Начальное приветствие
    /weather - Узнать погоду
    /stop - Продолжить общение
    """)
@bot.message_handler(commands=['weather'])
def weather_start(message):
    bot.send_message(message.chat.id,"Погода так погода, какой город вам нужен?")
    bot.send_message(message.chat.id,"Что бы продолженить общение, введите команду - !stop")
    global start
    start=1

@bot.message_handler(commands=['stop'])
def weather_stop(message):
    bot.send_message(message.chat.id,"Продолжаем общение)")
    global start
    start=0



@bot.message_handler(content_types=["text"])
def dialog(message):
    if start == 1:
        chat_id = message.chat.id
        try:
            place = message.text
            main = owm.weather_at_place(place)
            global weather
            weather = main.get_weather()#ДОСТАЕМ ОТ СЮДА ВСЮ ИНФУ, а так выглядит  прост как код!
            bot.send_message(chat_id, "Какую информацию о погоде вы хотели бы знать?", reply_markup=keyboard())
        except(api_response_error.NotFoundError):
            if message.text == "Макс.Темп" or message.text == "Средняя Темп" or message.text == "Мин.Темп" or message.text == "Скорость ветра" or message.text == "Детал Инф." or message.text == "Влажность":
                maxtemp = weather.get_temperature("celsius")["temp_max"]#выбор еденици исчесления, и функци
                midtemp =  weather.get_temperature("celsius")["temp"]#Средняя темп
                mintemp = weather.get_temperature("celsius")["temp_min"]#мин темп 
                speedwind = weather.get_wind()["speed"]#Ветер
                status = weather.get_detailed_status()#Стастус - детальный
                vlag = weather.get_humidity()#функция принимает инфу о влажности

                if message.text == "Макс.Темп":
                    bot.send_message(chat_id,"Максимальная Температура в районе - ({:.0f}".format(maxtemp)+"°C)", reply_markup=keyboard())
                elif message.text == "Средняя Темп":
                    bot.send_message(chat_id,"Средняя Температура в районе - ({:.0f}".format(midtemp)+"°C)", reply_markup=keyboard())
                elif message.text == "Мин.Темп":
                    bot.send_message(chat_id,"Минимальная Температура в районе - ({:.0f}".format(mintemp)+"°C)", reply_markup=keyboard())
                elif message.text == "Скорость ветра":
                    bot.send_message(chat_id,"Скорость ветра - {:.0f}".format(speedwind)+"м/с", reply_markup=keyboard())
                elif message.text == "Детал Инф.":
                    bot.send_message(chat_id,"На данный момент - "+status, reply_markup=keyboard())
                elif message.text == "Влажность":
                    bot.send_message(chat_id,"На данный момент влажность состовляет - {:.0f}".format(vlag)+"%", reply_markup=keyboard())
            else:
                bot.send_message(chat_id,"Ваш запрос не правильный, повторите попытку снова")
    else:
        request = apiai.ApiAI('30113feb0e2c4c9cbc5fe10f8c6148bd').text_request() # Токен API к Dialogflow
        request.lang = 'ru' # На каком языке будет послан запрос
        request.query = message.text # Посылаем запрос к ИИ с сообщением от юзера
        request.session_id = 'BatlabAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем отве
        if response:
            bot.reply_to(message, response)
        else:
            bot.send_message(message.chat.id,'Я Вас не совсем понялa!')

    
def keyboard():

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True) 
    knop1,knop2,knop3,knop4,knop5,knop6=types.KeyboardButton("Макс.Темп"),types.KeyboardButton("Средняя Темп"),types.KeyboardButton("Мин.Темп"),types.KeyboardButton("Скорость ветра"),types.KeyboardButton("Детал Инф."),types.KeyboardButton("Влажность")   
    markup.add(knop1,knop2,knop3)
    markup.add(knop4,knop5,knop6)
    return markup
    
while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(20)