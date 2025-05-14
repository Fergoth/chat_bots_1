import time
import requests
from dotenv import load_dotenv
import os
import logging
import telegram


logger = logging.getLogger(__file__)


class TelegramLogsHandler(logging.Handler):
    def __init__(self, chat_id, tg_token):
        super().__init__()
        self.chat_id = chat_id
        self.bot = telegram.Bot(token=tg_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def request_notification(headers, timestamp):
    devman_url = "https://dvmn.org/api/long_polling/"
    params = {"timestamp": timestamp}
    response = requests.get(devman_url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    tg_token = os.environ["TELEGRAM_BOT_TOKEN"]
    tg_debug_token = os.environ.get("TELEGRAM_DEBUG_BOT_TOKEN")
    if tg_debug_token:
        logger.addHandler(TelegramLogsHandler(chat_id, tg_debug_token))
    logger.setLevel(logging.INFO)
    logger.info("Бот запущен")
    bot = telegram.Bot(token=tg_token)
    timestamp = time.time()
    dvmn_token = os.environ["DEVMAN_TOKEN"]
    headers = {"Authorization": f"Token {dvmn_token}"}
    while True:
        try:
            response = request_notification(headers, timestamp)
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
            continue
        except requests.exceptions.ConnectionError:
            logger.error("Ошибка соединения, жду 5 секунд и повторяю запрос")
            time.sleep(5)
        except requests.HTTPError as e:
            logger.error(f"Сервер вернул код ошибки:{e}")
            time.sleep(5)
        except Exception as e:
            logger.error(f"Неизвестная ошибка:{e}")
            time.sleep(5)


if __name__ == "__main__":
    print(main())
