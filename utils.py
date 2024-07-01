from telebot import types
from constants import CHANNELS


def add_subscriptions_buttons(markup):
    for channel in CHANNELS:
        markup.add(types.InlineKeyboardButton(f'Подписаться на {channel["name"]}', url=channel['link']))
    markup.add(types.InlineKeyboardButton('Проверить подписки', callback_data='check_subs'))


def add_start_layout_buttons(markup):
    markup.add(types.InlineKeyboardButton('Начать играть', callback_data='start_game'))
    markup.add(types.InlineKeyboardButton('Авторы', callback_data='show_authors'))


START_LAYOUT_MESSAGE = "Нажмите 'Начать играть', чтобы начать новую игру, или 'Авторы', чтобы узнать об авторах."
