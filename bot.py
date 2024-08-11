
import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types
from datetime import datetime
import pytz
import re


def get_curs():
    response = requests.get("https://bluedollar.net/informal-rate/")
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')

        sell_blue_dollar = soup.find('div', class_='sell buy-sell-blue').text.strip()
        buy_blue_dollar = soup.find('div', class_='buy buy-sell-blue').text.strip()

        sell_blue_dollar = re.search(r'\d\S\d*\S\d*', sell_blue_dollar).group()
        buy_blue_dollar = re.search(r'\d\S\d*\S\d*', buy_blue_dollar).group()
        return sell_blue_dollar, buy_blue_dollar
    else:
        return "В данный момент сайт не отвечает, повторите свой вопрос позже!"

bot = telebot.TeleBot(token='33333#33333')
photo_url = "https://assets.sbnation.com/assets/2527405/Screen_Shot_2013-04-24_at_1.51.42_PM.png"


@bot.message_handler(commands=['start'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Узнать курс 💲", callback_data="foo"))
    bot.send_photo(message.chat.id, photo=photo_url, caption=f"Привет {message.from_user.first_name}!\n\nЧтобы узнать актуальный курс просто нажми кнопку 👇", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_message(call):
    user_id = call.message.chat.id
    sell, buy = get_curs()
    argentina_timezone = pytz.timezone('America/Argentina/Buenos_Aires')
    current_date = datetime.now(argentina_timezone).strftime("%d.%m.%Y")
    if call.data == "foo":
        print(f"Проверка курса {user_id}")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Узнать курс 💲", callback_data="foo"))
        bot.send_message(call.message.chat.id, f'<b>Курс на {current_date} год:</b>\n\n<b>Продажа:</b> {sell} PESOS\n<b>Покупка:</b> {buy} PESOS\n\n@bitbaires - Ваш надежный партнер в обмене валют.\n@ZhestPoArgentinski - важные новости Аргентины.\n\nЧтобы проверить курс еще раз нажми Узнать курс 💲 👇', parse_mode="html",  reply_markup=markup)


bot.polling(none_stop=True)




