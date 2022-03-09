import telebot
from config import keys, TOKEN
from extensions import ConvertException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text ='Чтобы начать работу введите команду боту\n в следуещем формате : \n ' \
        'имя валюты \ в какую перевести\ сколько перевести \n' \
        'список доступных валют: /values '
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text='Доступные валюты'
    for key in keys.keys():
        text='\n'.join((text, key, ))
    bot.reply_to(message,text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertException('не верный формат запроса используйте /help')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount) * float(amount)
    except ConvertException as e:
        bot.reply_to(message, f'ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} будет {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)