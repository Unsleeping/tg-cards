from telebot import types
import os
import random
import logging

from constants import START_LAYOUT_MESSAGE
from init import bot
from utils import add_subscriptions_buttons, add_start_layout_buttons, get_unsubscribed_channels, \
    check_subscriptions
from config import path_to_authors_image, cards_dir

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton('/start')
    keyboard.add(start_button)

    markup = types.InlineKeyboardMarkup()
    unsubscribed_channels = get_unsubscribed_channels(message.from_user.id)

    if len(unsubscribed_channels) == 0:
        add_start_layout_buttons(markup)
        bot.send_message(message.chat.id, START_LAYOUT_MESSAGE,
                         reply_markup=markup)
    else:
        add_subscriptions_buttons(markup, unsubscribed_channels)
        bot.send_message(message.chat.id, "Привет! Подпишитесь на следующие каналы, чтобы начать игру:",
                         reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'show_authors')
def show_authors(call):
    authors_image = path_to_authors_image
    if os.path.exists(authors_image):
        with open(authors_image, 'rb') as f:
            markup = types.InlineKeyboardMarkup()
            add_start_layout_buttons(markup)

            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_photo(call.message.chat.id, f, reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, "Изображение с авторами не найдено.")


@bot.callback_query_handler(func=lambda call: call.data == 'check_subs')
def check_subs(call):
    if check_subscriptions(call.from_user.id):
        markup = types.InlineKeyboardMarkup()
        add_start_layout_buttons(markup)

        bot.edit_message_text(f'Вы подписаны на все необходимые каналы! {START_LAYOUT_MESSAGE}', call.message.chat.id,
                              call.message.message_id,
                              reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        add_subscriptions_buttons(markup, unsubscribed_channels=get_unsubscribed_channels(call.from_user.id))

        bot.edit_message_text("Вы не подписаны на все необходимые каналы. Пожалуйста, подпишитесь и "
                              "попробуйте снова:", call.message.chat.id, call.message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'start_game')
def start_game(call):
    send_question(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == 'next_question')
def next_question(call):
    send_question(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == 'stop_game')
def stop_game(call):
    markup = types.InlineKeyboardMarkup()
    add_start_layout_buttons(markup)

    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, START_LAYOUT_MESSAGE, reply_markup=markup)


def send_question(chat_id, message_id):
    files = os.listdir(cards_dir)
    image_files = [file for file in files if file.endswith('jpg')]

    if not image_files:
        bot.send_message(chat_id, "Карточки не найдены")
        return

    random_image = random.choice(image_files)
    with open(os.path.join(cards_dir, random_image), 'rb') as f:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Далее', callback_data='next_question'))
        markup.add(types.InlineKeyboardButton('Стоп', callback_data='stop_game'))

        bot.delete_message(chat_id, message_id)
        bot.send_photo(chat_id, f, reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
