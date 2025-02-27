# XKCD comics publisher

Этот бот загружает случайный комикс [XKCD](https://xkcd.com/) и публикует его в Telegram.

## Установка и настройка

Установите зависимости:

```shell
pip install -r requirements.txt
```

Создайте файл `.env` в корневой папке вашего проекта и добавьте в него переменные:

```
TG_BOT_TOKEN='your_token'
TG_CHAT_ID='your_chat_id'
```
Для работы с Telegram-ботом необходимо создать бота через [BotFather](https://telegram.me/BotFather) и получить токен. 
Укажите этот токен в переменной окружения `TG_BOT_TOKEN`. 
Также укажите `TG_CHAT_ID`, который можно получить из Telegram (например, через `@userinfobot`).
## Использование

Запустите скрипт:

```shell
python main.py
```

Скрипт опубликует случайный комикс XKCD с подписью (при её наличии) в Telegram.
