import os
import random
from urllib.parse import urlparse

import requests
import telegram
from environs import Env


def download_and_save_image(image_url, filename):
    """Скачивает и сохраняет изображение по URL."""
    response = requests.get(image_url)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


def get_comic_json(url):
    """Получает JSON-ответ с комиксом XKCD."""
    response = requests.get(url)
    response.raise_for_status()
    comic_json = response.json()

    return comic_json


def fetch_random_xkcd_comic():
    """Загружает случайный комикс XKCD и скачивает изображение."""
    last_comic_url = 'https://xkcd.com/info.0.json'
    last_comic_id = get_comic_json(last_comic_url)['num']

    random_comic_id = random.randint(1, last_comic_id)
    random_comic_url = f'https://xkcd.com/{random_comic_id}/info.0.json'

    comic_json = get_comic_json(random_comic_url)

    image_url = comic_json['img']
    caption = comic_json['alt']

    filename = os.path.basename(urlparse(image_url).path)
    download_and_save_image(image_url, filename)

    return filename, caption


def send_photo_to_telegram(bot, chat_id, photo_path, caption=None):
    """Отправляет изображение в Telegram и удаляет его после отправки."""
    with open(photo_path, 'rb') as file:
        bot.send_photo(
            chat_id=chat_id,
            photo=file,
            caption=caption
        )
    os.remove(photo_path)


def main():
    """Главная функция: загружает XKCD и отправляет в Telegram."""
    env = Env()
    env.read_env()

    token = env.str('TG_BOT_TOKEN')
    chat_id = env.str('TG_CHAT_ID')

    bot = telegram.Bot(token=token)

    try:
        photo_path, caption = fetch_random_xkcd_comic()
        send_photo_to_telegram(bot, chat_id, photo_path, caption)

    except requests.exceptions.RequestException as error:
        print(f"Ошибка при загрузке комикса: {error}")
    except telegram.error.TelegramError as error:
        print(f"Ошибка при отправке в Telegram: {error}")


if __name__ == '__main__':
    main()
