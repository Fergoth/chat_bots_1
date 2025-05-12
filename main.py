import time
import requests
from dotenv import load_dotenv
import os
import logging
import telegram

logger = logging.getLogger(__file__)


def long_poll_devman(headers, timestamp):
    devman_url = "https://dvmn.org/api/long_polling/"
    params = {"timestamp": timestamp}
    response = requests.get(devman_url, headers=headers, params=params)
    return response.json()


def main():
    logger.setLevel(logging.INFO)
    load_dotenv()
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    bot = telegram.Bot(token=TG_TOKEN)
    timestamp = time.time()

    DEVMAN_TOKEN = os.getenv("DEVMAN_TOKEN")
    headers = {"Authorization": f"Token {DEVMAN_TOKEN}"}
    while True:
        try:
            response = long_poll_devman(headers, timestamp)
            status = response["status"]
            logger.debug(f"Ответ: {response}")
            if status == "timeout":
                logger.info("Нет активных проверок, повторяю запрос")
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
                        f"Ссылка на урок: {lesson_url}",
                    )
                timestamp = response["last_attempt_timestamp"]
        except requests.exceptions.ReadTimeout:
            logger.info("Таймаут, повторяю запрос")
        except requests.exceptions.ConnectionError:
            logger.info("Ошибка соединения, жду 5 секунд и повторяю запрос")
            time.sleep(5)


if __name__ == "__main__":
    print(main())
