import os
import random
from urllib.parse import urlparse

import requests
import telegram
from environs import Env


def download_image(url, filename):
    """Скачивает изображение по указанному URL и сохраняет его в файл."""
    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


def get_random_xkcd_comic():
    """Выбирает случайный комикс XKCD, загружает его изображение и описание."""

    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    last_comic_id = response.json()['num']

    random_comic_id = random.randint(1, last_comic_id)
    random_comic_url = f'https://xkcd.com/{random_comic_id}/info.0.json'

    response = requests.get(random_comic_url)
    response.raise_for_status()

    comic_image_url = response.json()['img']
    comic_caption = response.json()['alt']

    filename = os.path.basename(urlparse(comic_image_url).path)
    download_image(comic_image_url, filename)

    return filename, comic_caption


def send_image_to_telegram(bot, chat_id, path, caption=None):
    """Отправляет изображение в указанный Telegram-чат."""
    with open(path, 'rb') as file:
        bot.send_photo(
            chat_id=chat_id,
            photo=file,
            caption=caption
        )


def main():
    """Главная функция: Загружает случайный комикс XKCD и отправляет его в Telegram."""
    env = Env()
    env.read_env()

    token = env.str('TG_BOT_TOKEN')
    chat_id = env.str('TG_CHAT_ID')

    bot = telegram.Bot(token=token)

    image_path = None

    try:
        image_path, caption = get_random_xkcd_comic()
        send_image_to_telegram(bot, chat_id, image_path, caption)
    except requests.exceptions.RequestException as error:
        print(f"Ошибка при загрузке комикса: {error}")
    except telegram.error.TelegramError as error:
        print(f"Ошибка при отправке в Telegram: {error}")
    finally:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)


if __name__ == '__main__':
    main()
