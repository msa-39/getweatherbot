import requests
import time
import locale
import config

locale.setlocale(locale.LC_ALL, 'Russian_Russia.1251')

OpenWeatherAppID = config.OWAppID

# Определение направление ветра
def get_wind_direction(deg):
    l0 = ['\u21d1', '\u21d7', '\u21db', '\u21d8', '\u21d3', '\u21d9', '\u21da', '\u21d6']
    l1 = ['С ','СВ',' В','ЮВ','Ю ','ЮЗ',' З','СЗ']
    for i in range(0,8):
        step = 45.
        min = i*step - 45/2.
        max = i*step + 45/2.
        if i == 0 and deg > 360-45/2.:
            deg = deg - 360
        if deg >= min and deg <= max:
            res = l0[i] + l1[i]
            break
    return res

# Проверка наличия в базе информации о нужном населенном пункте
def get_city_id(s_city_name):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                     params={'q': s_city_name, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': OpenWeatherAppID})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]

        print('city:', cities)

        if len(cities) != 0:
            city_id = data['list'][0]['id']
            assert isinstance(city_id, int)
        else:
            city_id = None

        print('city_id =', city_id)

    except Exception as e:
        logging.exception("Exception (find): " + e)
        city_id = None
        pass

    return city_id

# Запрос текущей погоды
def request_current_weather(city_id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': OpenWeatherAppID})
        data = res.json()
        #print("data:", data)
        print('city:', data['name'], data['sys']['country'])

        c_mes = data['name'] + ", " + data['sys']['country'] + "\n\n"
        c_mes = c_mes + time.strftime('%a %d/%m/%Y',time.localtime(data['dt'])) + " " + data['weather'][0]['description'] + " " + '{0:+2.0f}'.format(data['main']['temp']) + "℃" + "\n"
        c_mes = c_mes + "В течении дня " + '{0:+2.0f}'.format(data['main']['temp_min']) + "..." + '{0:+2.0f}'.format(data['main']['temp_max']) + "℃" + "\n"
        c_mes = c_mes + "Ветер: " + '{0:2.0f}'.format(data['wind']['speed']) + " м/с " + get_wind_direction(data['wind']['deg']) + "\n"
        c_mes = c_mes + "Давление: " + '{0:4.0f}'.format(round(data['main']['pressure']*0.7500637554192)) + " мм рт.ст." + "\n"
        c_mes = c_mes + "Влажность: " + '{0:3.0f}'.format(data['main']['humidity']) + "%" + "\n"
        c_mes = c_mes + "Восход: " + time.strftime('%H:%M',time.localtime(data['sys']['sunrise'])) + "\n"
        c_mes = c_mes + "Закат: " + time.strftime('%H:%M', time.localtime(data['sys']['sunset']))

    except Exception as e:
        print("Exception (weather):", e)
        pass

    return c_mes

# Прогноз на 5 дней
def request_forecast_daily(city_id, ddate):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast/daily",
                     params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': OpenWeatherAppID})
        data = res.json()
        #print("data:", data)
        print('city:', data['city']['name'], data['city']['country'])
        c_mes = data['name'] + ", " + data['sys']['country'] + "\n\n"

        for i in data['list']:
           if ddate == "all" or ddate == time.strftime('%d/%m/%Y',time.localtime(i['dt'])):
             c_mes = c_mes + time.strftime('%a %d/%m/%Y',time.localtime(i['dt'])) + " " + i['weather'][0]['description'] + " " + '{0:+2.0f}'.format(i['temp']['min']) + "..." + '{0:+2.0f}'.format(i['temp']['max']) + "℃" + "\n"
             c_mes = c_mes + "Ночью: " + '{0:+2.0f}'.format(i['temp']['night']) + "℃" + "\n"
             c_mes = c_mes + "Утром: " + '{0:+2.0f}'.format(i['temp']['morn']) + "℃" + "\n"
             c_mes = c_mes + "Днем: " + '{0:+2.0f}'.format(i['temp']['day']) + "℃" + "\n"
             c_mes = c_mes + "Вечером: " + '{0:+2.0f}'.format(i['temp']['eve']) + "℃" + "\n"
             c_mes = c_mes + "Ветер: " + '{0:2.0f}'.format(i['speed']) + " м/с " + get_wind_direction(i['deg']) + "\n"
             c_mes = c_mes + "Давление: " + '{0:4.0f}'.format(round(i['pressure']*0.7500637554192)) + " мм рт.ст." + "\n"
             c_mes = c_mes + "Влажность: " + '{0:3.0f}'.format(i['humidity']) + "%" + "\n\n"

    except Exception as e:
      print("Exception (forecast):", e)
      pass
    return c_mes

# Прогноз по часам
def request_forecast(city_id, ddate):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': OpenWeatherAppID})
        data = res.json()
        #print("data:", data)
        print('city:', data['city']['name'], data['city']['country'])
        c_mes = data['name'] + ", " + data['sys']['country'] + "\n\n"

        for i in data['list']:
          if ddate == "all" or ddate == time.strftime('%d/%m/%Y', time.localtime(i['dt'])):
            c_mes = c_mes + \
                    time.strftime('%d/%m/%Y %H:%M', time.localtime(i['dt'])) + " " + \
                    '{0:+2.0f}'.format(i['main']['temp']) + "℃ " + \
                    '{0:2.0f}'.format(i['wind']['speed']) + " м/с " + \
                    get_wind_direction(i['wind']['deg']) + " " + \
                    i['weather'][0]['description'] + "\n"

    except Exception as e:
        print("Exception (forecast):", e)
        pass
    return c_mes