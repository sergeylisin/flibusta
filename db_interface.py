import logging
from pycountry import db
from db import db_session
from model import ZipFile, Book, Word, BookWord, WordTemp
import zip_file
import book
from typing import List, Set, Iterable
from sqlalchemy.exc import IntegrityError
import tokenizer


class NoSuchWord(Exception):
    pass


def commit():
    db_session.commit()

def rollback():
    db_session.rollback()

def save_zip_file(zipfile: zip_file.ZipFile) -> ZipFile:
    z = ZipFile(zip_name=zipfile.zip_name)
    try:
        db_session.add(z)
        db_session.commit()
    except IntegrityError as e:
        db_session.rollback()
        logging.error(e)
    return z


def save_book(book: book.Book) -> Book:
    db_book = Book(zip_name=book.zip_file.zip_name, book_name=book.book_name, title=book.title,
                   annotation=book.annotation, authors=book.authors, language=book.lang)
    try:
        db_session.add(db_book)
        db_session.commit()
    except IntegrityError as e:
        db_session.rollback()
        db_book = db_session.query(Book).filter(
            Book.zip_name == book.zip_file.zip_name and Book.book_name == book.book_name).first()
        logging.error(e)
    for word in book.words:
        save_book_word(db_book, word)
    db_session.commit()
    return db_book


def save_book_word(book: Book, word: str):
    db_word = Word(word=word, cnt=1)
    try:
        db_session.add(db_word)
        db_session.commit()
    except IntegrityError as e:
        db_session.rollback()
        db_session.query(Word).filter(
            Word.word == word).update({Word.cnt: Word.cnt + 1})
        db_word = db_session.query(Word).filter(Word.word == word).first()
    db_book_word = BookWord(book_id=book.id, word_id=db_word.id)
    try:
        db_session.add(db_book_word)
        db_session.commit()
    except IntegrityError as e:
        db_session.rollback()


def get_word_id(word: str) -> int:
    db_word = db_session.query(Word).filter(Word.word == word).first()
    if db_word == None:
        return None
    return db_word.id


def get_words_id(words: Iterable[str]) -> Iterable[str]:
    return filter(lambda x: x != None, map(lambda w: get_word_id(w), words))

    
