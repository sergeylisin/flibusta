import settings
import search
import book as b
import db_interface

import telegram.ext
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters
from typing import List, Iterable
from pprint import pprint
import re


session = None

BOOK_INFO_REGEXP = '^/info(\d+)'
BOOK_GET_REGEXP = '^/get(\d+)'


def greet_user(update: Update, context: CallbackContext):
    global session
#    pprint(update.message.from_user.id)
    session = search.SearchSession(p_user_id=update.message.from_user.id)


def search_book(update: Update, context: CallbackContext):
    global session
    if session == None:
        session = search.SearchSession(update.message.from_user.id)
    session.search(update.message.text)
    text = "\n".join(map(
        lambda x: f"{x.authors} - {x.title} /info{x.book_name}", session.search_result))
    update.message.reply_text(text)


def book_info(update: Update, context: CallbackContext):
    r = re.findall(BOOK_INFO_REGEXP, update.message.text)
    if len(r) > 0:
        book = db_interface.get_book(book_name=r[0])
        reply_text = book.annotation + "\n" + f"/get{book.book_name}"
        update.message.reply_text(reply_text)
    else:
        update.message.reply_text("unknown book")


def get_book(update: Update, context: CallbackContext):
    r = re.findall(BOOK_GET_REGEXP, update.message.text)
    if len(r) > 0:
        book = db_interface.get_book(book_name=r[0])
        update.message.reply_text(book.annotation)
    else:
        update.message.reply_text("unknown book")


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(RegexHandler(BOOK_INFO_REGEXP, book_info))
    dp.add_handler(RegexHandler(BOOK_GET_REGEXP, get_book))
    dp.add_handler(MessageHandler(Filters.text, search_book))

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
