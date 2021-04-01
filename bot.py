import settings
import search
from book import Book

import telegram.ext
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters
from typing import List, Iterable
from pprint import pprint


session = None


def greet_user(update: Update, context: CallbackContext):
    global session
#    pprint(update.message.from_user.id)
    session = search.SearchSession(p_user_id=update.message.from_user.id)


def search_book(update: Update, context: CallbackContext):
    global session
    if session == None:
        session = search.SearchSession(update.message.from_user.id)
    search_text = update.message.text[update.message.text.find(' ')+1:]
    session.search(search_text)
    text = "\n".join(map(lambda x : f"{x.authors} - {x.title} /info{x.book_name}",session.search_result))
    update.message.reply_text(text)


def book_info(update: Update, context: CallbackContext):
    update.message.reply_text(update.message.text)


def get_book(update: Update, context: CallbackContext):
    print(update.message.text[update.message.text.find(' ')+1:])
    update.message.reply_text(update.message.text)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(RegexHandler('^/info\d+', book_info))
    dp.add_handler(RegexHandler('^/get\d+', get_book))
    dp.add_handler(MessageHandler(Filters.text,search_book))


    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
