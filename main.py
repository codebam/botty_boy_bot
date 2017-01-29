#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
from uuid import uuid4

from telegram import InlineQueryResultArticle, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import logging
from urllib.parse import quote_plus
import configparser
from os import environ
import requests
import json

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='''Hello, I am a bot that matches you with people of the same interests. To start talking to others, you may ask a question with /ask. Otherwise, you can subscribe to updates from other users with /subscribe.''')


def new_user(userID):
    with open('userdata.json', 'r') as f: # read file
        json_data = json.load(f)
    user = { 'userID' : userID }
    for _user in json_data['Users']:
        if (_user.get("userID") == userID): # if the user isn't already in the list
            return False
    return True


def add_user(userID):
    if new_user(userID):
        json_data['Users'].append(user)
    with open('userdata.json', 'w') as f: # write file
        json.dump(json_data, f)


def modify_user(bot, update):
    if new_user(update.message.from_user.id):
        bot.sendMessage(update.message.chat_id, text='''Please use /subscribe before trying to modify user settings.''')


def subscribe(bot, update):
    add_user(update.message.from_user.id)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def change_token():
    config = []
    config['config'] = {'token': input('API Key: ')}
    if input('Save? [Y/n]') not in ['n', 'N']:
        with open('config.mine.ini', 'w') as configfile:
            config.write(configfile)
        print('API Key Saved to config.mine.ini')
    return config['config']['token']


def main():
    try:
        token_ = environ['TELEGRAM_API_KEY']
        # tries to read the api key inside an environment var if it exists
    except KeyError:
        config = configparser.ConfigParser()
        config.read('config.mine.ini')
        try:
            token_ = config['config']['token']
        except KeyError:
            config.read('config.ini')
            try:
                token_ = config['config']['token']
            except:
                pass
            # if there's a keyerror the file probably doesn't exist
            # we fall back to config.ini (the template file)

    if token_ in ['','enter your token here']:
        token_ = change_token()
        # if both token files are empty we prompt the user to enter
        # their api key and optionally save it

    # Create the Updater and pass it your bot's token.
    updater = Updater(token_)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("subscribe", subscribe))

    # on noncommand i.e message - echo the message on Telegram

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
