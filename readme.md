# Отправка сообщений и стикеров от бота в Телеграме

## Перед началом работы
1. Внесите токен существующего Телеграм-бота в файл config.yaml (раздел telegram --> bot1). Нового бота можно завести, написав в Телеграме сообщение @BotFather.
2. Установите библиотеку для работы с Telegram API (https://github.com/python-telegram-bot/python-telegram-bot). В командной строке выполните:
	pip install python-telegram-bot --upgrade
3. Узнайте параметр chat_id и запишите его в файл config.yaml (раздел users, пользователя "default" с chat_id 0 лучше оставить). Для этого напишите любое сообщение вашему боту. Затем запустите файл get_chat_id.py:
	```
	python get_chat_id.py
	Last message chat ID: 121314151 Ivan Ivanov
	```

	Например:
	```
	users:
	    me: 121314151
	    default: 0
	```

## Быстрый старт:
```python
from telegramNotifier import notifierClass

mess = notifierClass( 'me' )
mess.notification( 'Посчиталось ура' )
mess.sticker()
```

## Отправка стикеров
Вы можете создать свой набор стикеров на подходящие вам ситуации. Для этого в файле config.yaml внесите любое стикера и его file_id. Чтобы узнать file_id стикера, отправьте этот стикер боту. Затем запустите файл get_chat_id.py:

```
python get_chat_id.py
Sticker file_id CAADAgADQAADyIsGAAE7MpzFPFQX5QI
Last message chat ID: 121314151 Ivan Ivanov
```

Вносим полученный file_id в файл config.yaml:
```
stickers:
    default: CAADAgADOQEAAjbsGwVonn-MGIBY3AI
    success: CAADAgADQAADyIsGAAE7MpzFPFQX5QI
```

Теперь можно отправить данный стикер из скрипта:
```python
from telegramNotifier import notifierClass

mess = notifierClass( 'me' )
mess.sticker( sticker = 'success' )
```