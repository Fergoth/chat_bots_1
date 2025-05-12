# Чат бот для отслеживания проверок по проверке заданий на сайте dvmn.org



## Окружение
### Требования
Для запуска требуется python версии 3.13. Или установленная утилита [uv](https://docs.astral.sh/uv/) 



### Установка зависимостей (если нет uv) 
```sh
pip install -r requirements.txt
```
### Переменные окружения

- DEVMAN_TOKEN
- TELEGRAM_BOT_TOKEN

1. Создайте файл `.env` около `main.py`.
2. Заполните файл `.env` следующим образом без кавычек:
```bash
DEVMAN_TOKEN=asfgafgadfg495
TELEGRAM_BOT_TOKEN=afgafgafg49
TELEGRAM_CHAT_ID=21341234
```
#### Как получить токены

*  Токен для Девмана  DEVMAN_TOKEN можно получить по [ссылке](https://dvmn.org/api/docs/)
*  Токен для телеграм бота TELEGRAM_BOT_TOKEN можно получить при создании бота [ссылке](https://telegram.me/BotFather)
* TELEGRAM_CHAT_ID - ваш айди в телеграме, можно получить у [бота](https://telegram.me/userinfobot) 

### Запустите скрипт 
```sh
python main.py 
```
Где chat_id - ваш айди в телеграме, можно получить у [бота](https://telegram.me/userinfobot) 
### При наличии uv
- Просто запустите скрипт с помощью uv 
```sh
uv run main.py 
```

### Примечание
  Напишите боту чтобы он мог отправлять вам сообщения
