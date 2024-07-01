from telebot import types
import os
import telebot
import random
from config import token, path_to_authors_image, cards_dir
from constants import CHANNELS
import logging

from utils import add_subscriptions_buttons, add_start_layout_buttons, START_LAYOUT_MESSAGE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(token)


def check_subscriptions(user_id):
    # return False
    for channel in CHANNELS:
        try:
            member = bot.get_chat_member('@' + channel['link'].split('/')[-1], user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except telebot.apihelper.ApiException as e:
            if 'member list is inaccessible' in str(e):
                logger.error(f"Error checking subscription for {channel['link']}: Bot needs to be an admin to access "
                             f"the member list.")
            else:
                logger.error(f"Error checking subscription for {channel['link']}: {e}")
            return False
    return True


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    add_subscriptions_buttons(markup)
    bot.send_message(message.chat.id, "Привет! Подпишитесь на следующие каналы, чтобы начать игру:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'show_authors')
def show_authors(call):
    authors_image = path_to_authors_image
    if os.path.exists(authors_image):
        with open(authors_image, 'rb') as f:
            bot.send_photo(call.message.chat.id, f)
    else:
        bot.send_message(call.message.chat.id, "Изображение с авторами не найдено.")

    markup = types.InlineKeyboardMarkup()
    add_start_layout_buttons(markup)
    bot.send_message(call.message.chat.id,
                     START_LAYOUT_MESSAGE,
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'check_subs')
def check_subs(call):
    if check_subscriptions(call.from_user.id):
        markup = types.InlineKeyboardMarkup()
        add_start_layout_buttons(markup)
        bot.edit_message_text("Вы подписаны на все необходимые каналы! Нажмите 'Начать игру' чтобы начать или "
                              "'Авторы' чтобы узнать об авторах.", call.message.chat.id, call.message.message_id,
                              reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        add_subscriptions_buttons(markup)
        bot.send_message(call.message.chat.id, "Вы не подписаны на все необходимые каналы. Пожалуйста, подпишитесь и "
                                               "попробуйте снова:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'start_game')
def start_game(call):
    bot.edit_message_text("Игра началась! Вот ваша первая карточка:", call.message.chat.id, call.message.message_id)
    send_question(call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == 'next_question')
def next_question(call):
    send_question(call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == 'stop_game')
def stop_game(call):
    bot.edit_message_text("Игра остановлена. Если хотите начать снова, нажмите 'Начать играть'.", call.message.chat.id, call.message.message_id)
    markup = types.InlineKeyboardMarkup()
    add_start_layout_buttons(markup)
    bot.send_message(call.message.chat.id, START_LAYOUT_MESSAGE, reply_markup=markup)


def send_question(chat_id):
    files = os.listdir(cards_dir)
    image_files = [file for file in files if file.endswith('jpg')]
    if not image_files:
        bot.send_message(chat_id, "Карточки не найдены")
        return
    random_image = random.choice(image_files)
    with open(os.path.join(cards_dir, random_image), 'rb') as f:
        bot.send_photo(chat_id, f)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Далее', callback_data='next_question'))
    markup.add(types.InlineKeyboardButton('Стоп', callback_data='stop_game'))
    bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
