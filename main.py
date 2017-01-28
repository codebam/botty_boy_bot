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

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='''Hello, I am an Inline bot, \
please use me by mentioning my username in a chat along with your query''')

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
