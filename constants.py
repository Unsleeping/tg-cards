DEBUG_CHANNELS = [
    {'name': 'Channel 1', 'link': 'https://t.me/crypto_farm_hub'},
    {'name': 'Channel 2', 'link': 'https://t.me/unsleeping706'},
    # {'name': 'Channel 3', 'link': 'https://t.me/cards_faster'}
]

REAL_CHANNELS = [
    {'name': 'НЦФМ | Национальный центр физики и математики', 'link': 'https://t.me/ncphm_sarov'},
    {'name': 'СНО МГУ Саров', 'link': 'https://t.me/msusarovssc'},
]

START_LAYOUT_MESSAGE = "Нажмите \"Начать играть\", чтобы начать новую игру, или \"Авторы\", чтобы узнать об авторах."

is_debug = False

CHANNELS = DEBUG_CHANNELS if is_debug else REAL_CHANNELS
