import logging
import telebot
from telebot import types

from constants import CHANNELS
from init import bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_subscriptions_buttons(markup, unsubscribed_channels):
    for channel in unsubscribed_channels:
        markup.add(types.InlineKeyboardButton(f'{channel["name"]}', url=channel['link']))
    markup.add(types.InlineKeyboardButton('Проверить подписки', callback_data='check_subs'))


def add_start_layout_buttons(markup):
    markup.add(types.InlineKeyboardButton('Начать играть', callback_data='start_game'))
    markup.add(types.InlineKeyboardButton('Авторы', callback_data='show_authors'))


def get_unsubscribed_channels(user_id):
    unsubscribed_channels = []
    for channel in CHANNELS:
        try:
            member = bot.get_chat_member('@' + channel['link'].split('/')[-1], user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                unsubscribed_channels.append(channel)
        except telebot.apihelper.ApiException as e:
            if 'member list is inaccessible' in str(e):
                logger.error(f"Error checking subscription for {channel['link']}: Bot needs to be an admin to access "
                             f"the member list.")
            else:
                logger.error(f"Error checking subscription for {channel['link']}: {e}")
    return unsubscribed_channels


def check_subscriptions(user_id):
    unsubscribed_channels = get_unsubscribed_channels(user_id)
    return len(unsubscribed_channels) == 0



