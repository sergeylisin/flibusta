import logging

from pycountry import db
from db import db_session
import model
import zip_file
import book
import typing
from sqlalchemy.exc import IntegrityError


def commit():
    db_session.commit()

def save_zip_file(zipfile:zip_file.ZipFile) -> model.ZipFile:
    z = model.ZipFile(zip_name=zipfile.zip_name)
    try:
        db_session.add(z)
        db_session.commit()
    except IntegrityError as e:
        db_session.rollback()
        logging.error(e)
    return z

def save_book(book:book.Book)->model.Book:
    db_book = model.Book(zip_name = book.zip_file.zip_name, book_name = book.book_name, title = book.title,\
        annotation = book.annotation, authors = book.authors,language = book.lang)
    try:
        db_session.add(db_book)
        for word in book.words:
            save_book_word(book,word)
        db_session.flush()
    except IntegrityError as e:
        db_session.rollback()
        logging.error(e)
    return db_book

def save_book_word(book:book.Book, word: str) -> model.Word:
    pass