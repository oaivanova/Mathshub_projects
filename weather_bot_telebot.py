import telebot
import requests
import json
import logging

if __name__ == '__main__':
    api_token = '5822987809:AAHNb46fH7cnIdx2J-ucn5rLBpZ2gvTOen8'

    bot = telebot.TeleBot(api_token)
    open_weather_api_key = '606129dccd5a9d42884a33d61df90ca3'

# добавим логгирование, чтобы получать сообщения в консоль
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

#def run_weather_bot(token: str) -> None:
#    """ Run bot that return current weather from https://openweathermap.org/"""
#    bot = telebot.TeleBot(token, parse_mode=None)

@bot.message_handler(commands=['start'])
def start_message(message):
        # пишет стартовое сообщение с именем пользователя
        bot.send_message(message.chat.id,
                         text=f'Привет, {message.from_user.username}! \n\nЯ - погодный бот! \nВведи название города, для которого хочешь узнать погоду  \n')

@bot.message_handler(content_types=['text'])
#@bot.message_handler(commands=['get_weather']):
def get_weather(message):
        # ответ на запрос о погоде
        #url = 'https://api.openweathermap.org/data/2.5/weather'
        city = message.text.strip().lower()
        # отправляем GET-запрос на URL-адрес API с заданными параметрами
        #params = {'q': city, 'appid': open_weather_api_key, 'units': 'metric'}
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_api_key}&units=metric')
        if res.status_code == 200:
            #data = res.json()
            data = json.loads(res.text)
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            weather_description = data["weather"]["main"]
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            bot.reply_to(message,
                         text=f'Сейчас в {city} {weather_description}, \nТемпература воздуха {temp}°С, ощущается как {feels_like}°С.\
                         \nСкорость ветра {wind}м/с.\
                         \nВлажность воздуха составляет {humidity}%.\
                         \nДавление {pressure} мм.рт.ст')
        else:
             bot.send_message(message.chat.id, 'Город не найден \U00002620')

bot.polling()
