import os

token = os.getenv("BOT_TOKEN")
path_to_authors_image = os.getenv("AUTHORS_IMAGE_PATH", "./images/authors.jpg")
cards_dir = os.getenv("CARDS_DIR", "./cards")
