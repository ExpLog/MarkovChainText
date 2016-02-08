#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.

"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import Updater
from markov.markovtext import MarkovChainText
import logging

class MarkovBot():
    def __init__(self, file, poll_size=20):
        self.file = open(file)
        self.generator = MarkovChainText(self.file)

        # Enable logging
        logging.basicConfig(
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                level=logging.INFO)

        self.logger = logging.getLogger(__name__)
        self.message_poll = []
        self.poll_size = poll_size


    # Define a few command handlers. These usually take the two arguments bot and
    # update. Error handlers also receive the raised TelegramError object in error.
    def help(self, bot, update):
        bot.sendMessage(update.message.chat_id, text='Help! I need somebody')

    def talk(self, bot, update):
        generated_text = self.generator.sample_phrases()
        print(generated_text)
        bot.sendMessage(update.message.chat_id, text=generated_text)

    def echo(self, bot, update):
        if len(self.message_poll) < self.poll_size:
            self.message_poll.append(update.message.text)
        else:
            #self.generator.update(self.message_poll)
            self.message_poll.clear()

    def error(self, update, error):
        self.logger.warn('Update "%s" caused error "%s"' % (update, error))

    def run(self):
        # Create the EventHandler and pass it your bot's token.
        updater = Updater("194949588:AAETiWnXkKaOipiu2jaKHWmcTWnPfHXLXf0")

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # on different commands - answer in Telegram
        dp.addTelegramCommandHandler("help", self.help)
        dp.addTelegramCommandHandler("talk", self.talk)

        # on noncommand i.e message - echo the message on Telegram
        dp.addTelegramMessageHandler(self.echo)

        # log all errors
        dp.addErrorHandler(self.error)

        # Start the Bot
        updater.start_polling()

        # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()

if __name__ == '__main__':
    bot = MarkovBot("../test/pg11.txt")
    bot.run()
