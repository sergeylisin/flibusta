import settings
import search
from book import Book

import telegram.ext
from telegram import ReplyKeyboardMarkup
from telegram.update import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from typing import List, Iterable


session = None


def get_keyboard(books: Iterable[Book]) -> ReplyKeyboardMarkup:
    menu = []
    for i in books:
        menu.append([f"/get {i.book_name}"])
    return ReplyKeyboardMarkup(menu)


def greet_user(update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext):
    session = search.SearchSession()


def search_book(update: Update, context: telegram.ext.callbackcontext.CallbackContext):
    global session
    if session == None:
        session = search.SearchSession()
    search_text = update.message.text[update.message.text.find(' ')+1:]
    session.search(search_text)
    text = "\n".join(map(lambda x:f"{x.book_name} {x.title}",session.search_result))
    update.message.reply_text(text, reply_markup=get_keyboard(session.search_result))
    


def get_book(update: Update, context: telegram.ext.callbackcontext.CallbackContext):
    print(update.message.text[update.message.text.find(' ')+1:])


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("search", search_book))
    dp.add_handler(CommandHandler("get", get_book))

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
