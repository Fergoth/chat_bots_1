import time
import requests
from dotenv import load_dotenv
import os
import logging
import telegram
import argparse

logging.basicConfig(level=logging.INFO)
load_dotenv()


def parse_chat_id():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "chat_id",
        help="Chat id  можно получить у бота: @userinfobot",
        type=int,
        )
    return parser.parse_args().chat_id


def long_poll_devman(headers, timestamp):
    devman_url = "https://dvmn.org/api/long_polling/"
    params = {"timestamp": timestamp}
    response = requests.get(devman_url, headers=headers, params=params)
    return response.json()


def main():
    chat_id = parse_chat_id()
    TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    bot = telegram.Bot(token=TG_TOKEN)
    timestamp = time.time()

    DEVMAN_TOKEN = os.getenv("DEVMAN_TOKEN")
    headers = {"Authorization": f"Token {DEVMAN_TOKEN}"}
    while True:
        try:
            response = long_poll_devman(headers, timestamp)
            status = response["status"]
            logging.debug(f"Ответ: {response}")
            if status == "timeout":
                logging.debug("Нет активных проверок, повторяю запрос")
                timestamp = response["timestamp_to_request"]
            elif status == "found":
                bot.send_message(chat_id=chat_id, text="Проверена новая работа!")
                for attempt in response["new_attempts"]:
                    title = attempt.get("lesson_title")
                    is_negative = attempt.get("is_negative")
                    attempt_status = "Провал :(" if is_negative else "Успешно :)"
                    lesson_url = attempt.get("lesson_url")
                    bot.send_message(
                        chat_id=chat_id,
                        text=f"Проверена работа '{title}' \n"
                        f"Статус проверки: {attempt_status}\n"
                        f"Ссылка на урок: {lesson_url}"
                    )
                timestamp = time.time()
        except requests.exceptions.ReadTimeout:
            logging.info("Таймаут, повторяю запрос")
        except requests.exceptions.ConnectionError:
            logging.info("Ошибка соединения, жду 5 секунд и повторяю запрос")
            time.sleep(5)


if __name__ == "__main__":
    print(main())
