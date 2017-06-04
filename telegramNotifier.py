# -*- coding: utf-8 -*-
# Устанавливаем библиотеку для работы с Telegram API
# https://github.com/python-telegram-bot/python-telegram-bot
# pip install python-telegram-bot --upgrade

import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler

from yaml import load
import os
import ast

class notifierClass:
    """
    Класс для отправки уведомлений от имени вашего бота
    Быстрый старт:
        ...

    Для отправки сообщений вы должны быть вписаны в список адресатов users. Чтобы внести себя в список узнайте свой chat_id с ботом:
        1. Начните диалог с ботом любым сообщением
        2. В питоне выполните команду analyticsTelegram('default').chatID(). Вам будет показан chat_id последнего диалога с ботом. Убедитесь, что соответствующее имя пользователя ваше. Скопируйте chat_id, выберите свой логин и пришлите на k.bashevoy@rambler-co.ru
        3. Как только ваш логин будет внесен в класс вы сможете отправлять уведомления
        4. Чтобы просмотреть текущий список пользователей выполните:
            print analyticsTelegram('default').users
    """

    def __init__( self, user = 'default' ):
        """
        """

        self.user = user

        # берем необходимые значения из файла config.yaml
        self.__checkUserInConfig()
        

    def __checkUserInConfig( self ):
        """
        Проверяем, есть ли пользователь в списке логинов. 
        Двойное подчеркивание в названии метода делает его приватным, т. е. недоступным вне класса. В данном случае это просто пример
        """

        # берем адрес текущей папки, где лежит класс
        # класс может вызываться из любой директории, а файл config.yaml лежит в текущей
        curr_path = os.path.dirname( os.path.realpath( __file__ ) )

        # импортируем токен и список пользователей из файла config.yaml
        with open( os.path.join( curr_path, 'config.yaml' ), 'r' ) as f:
            self.config = load( f )

        token = self.config['telegram']['bot1']['token']
        self.bot = telegram.Bot( token )

        self.users = self.config['users']

        # триггер, который включается только при правильном указании пользователя из словаря self.users
        # при значении self.ok = False метод notification не работает
        self.ok = False

        # проверяем есть ли пользователь с словаре
        if self.user in self.users:
            self.chat_id = self.users[ self.user ]
            self.ok = True

        else:
            # служебные сообщения по-английски, чтобы корректно отображались в разных командных строках
            print( 'No such user in list {}. \n Notification was not sent. Try again '.format( self.user ) )

    def chatID( self ):
        """
        Получение chat_id последнего сообщения боту

        Пример
        print( notifierClass().chatID() )

        Last message chat ID: 121314151 Ivan Ivanov
        """

        # получаем последнее сообщение бота update
        # update является объектом <class 'telegram.update.Update'>
        """
        { 'update_id': 453324194, 
          'message': {
            'message_id': 2, 
            'date': 1496499938, 
            'chat': {
                'id': 121314151, 
                'type': 'private', 
                'username': 'ivanivanov', 
                'first_name': 'Ivan', 
                'last_name': 'Ivanov'
            }, 

            'text': '/start', 
            'entities': 
                [
                    { 'type': 'bot_command', 
                      'offset': 0, 
                      'length': 6
                    }
                ], 

            'photo': [], 
            'new_chat_members': [], 
            'new_chat_photo': [], 
            'delete_chat_photo': False, 
            'group_chat_created': False, 
            'supergroup_chat_created': False, 
            'channel_chat_created': False, 
            'from': {
                'id': 133111680, 
                'first_name': 'Ivan', 
                'last_name': 'Ivanov', 
                'username': 'ivanivanov', 
                'language_code': 'ru'
            }, 

            'new_chat_member': None
          }
        }
        """
        update = self.bot.getUpdates()[-1]

        # преобразуем объект update в словарь updateDict
        updateDict = ast.literal_eval(str( update ) )

        # если последним сообщением был стикер, то выводим file_id
        if 'sticker' in updateDict['message']:
            print( 'Sticker file_id {}'.format( updateDict['message']['sticker']['file_id'] ) )

        return 'Last message chat ID: {} {} {}'.format( updateDict['message']['from']['id'], updateDict['message']['from']['first_name'], updateDict['message']['from']['last_name'] )

    def notification( self, message ):
        """
        Отправка сообщения message от имени бота. В текущей версии берутся первые 4000 символов, чтобы попасть в ограничения Телеграма

        Пример
        """

        # проверяем есть ли текущий пользователь в списке доступов config.yaml
        # если пользователя нет в списке доступов, то __checkUserInConfig выведет на экран сообщение
        self.__checkUserInConfig()

        if self.ok:
            self.bot.sendMessage( chat_id = self.chat_id, text = message[:4000] )

    def sticker( self, sticker = 'default' ):
        """
        Отправка сообщения message от имени бота. В текущей версии берутся первые 4000 символов, чтобы попасть в ограничения Телеграма

        Пример
        """

        # проверяем есть ли текущий пользователь в списке доступов config.yaml
        # если пользователя нет в списке доступов, то __checkUserInConfig выведет на экран сообщение
        self.__checkUserInConfig()

        if self.ok:
            if sticker in self.config['stickers']:
                self.bot.sendSticker( chat_id = self.chat_id, sticker = self.config['stickers'][ sticker ] )
