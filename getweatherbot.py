import owapi
import config
import telebot
from SQLighter import SQLighter
import time

#city_id for Kaliningrad
#city_id = 554234

#s_city_name = str(input())
#d_date = str(input())
#print("city:", s_city_name)
#city_id = owapi.get_city_id(s_city_name)

#print('Запрос текущей погоды')
#cur_weather = owapi.request_current_weather(city_id)
#print(cur_weather)
#print('')
#print('Запрос прогноза погоды на 5 дней')
#daily_weather = owapi.request_forecast_daily(city_id, d_date)
#print(daily_weather)
#print('')
#print('Запрос прогноза погоды по часам')
#hour_weather = owapi.request_forecast(city_id, d_date)
#print(hour_weather)

#@bot.message_handler(content_types=["text"])
#def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
#    bot.send_message(message.chat.id, message.text)

#b = time.time()
#print(b)
#print(time.strftime('%d/%m/%Y %H:%M', time.localtime(b)))

import logging

logger = telebot.logger
logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

bot = telebot.TeleBot(config.TelegrammBotKey)

@bot.message_handler(commands=['start'])
def start(message):

    print(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name, message.from_user.language_code)

    # Подключаемся к БД
    db_worker = SQLighter(config.database_name)

    row = db_worker.select_user_by_id(message.from_user.id)
    print(row)

    if len(row) == 0:
        db_worker.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name, message.from_user.language_code, "", time.time())

    # Отсоединяемся от БД
    db_worker.close()

    bot.send_message(message.chat.id, message.from_user.first_name + ", отправьте ваше местоположение или название города (латиницей).")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def get_answer(message):
    city_id = owapi.get_city_id(message.text)
    if city_id is not None:
        cur_weather = owapi.request_current_weather(city_id)
        bot.send_message(message.chat.id, cur_weather)
    else:
        bot.send_message(message.chat.id, message.from_user.first_name + ", Мы не смогли найти Ваш город! Попробуйте еще раз.")



#Теперь запустим бесконечный цикл получения новых записей со стороны Telegram:

if __name__ == '__main__':
    bot.polling(none_stop=True)
