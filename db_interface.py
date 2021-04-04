import logging
from db import db_session
from model import Session, ZipFile, Book, Word, BookWord, SearchResult, SearchWords, Session
import zip_file
import book
from typing import List, Set, Iterable
from sqlalchemy.exc import IntegrityError



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
    try:
        db_zipfile = ZipFile(zip_name = book.zip_file.zip_name)
        db_session.merge(db_zipfile)
        db_session.commit()
    except IntegrityError as e:
        db_session.rollback()
        db_zipfile = db_session.query(ZipFile).filter(
            ZipFile.zip_name == book.zip_file.zip_name).first()
        logging.error(e)
    db_book = Book(zip_name=book.zip_file.zip_name, book_name=book.book_name, title=book.title,
                   annotation=book.annotation, authors=book.authors, language=book.lang, genre = book.genre)
   
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


def get_book(book_name:str) -> Book:
    book = db_session.query(Book).filter(Book.book_name == book_name).first()
    return book

def get_search_words(p_session_id: int) -> Iterable[int]:
    ret = []
    for i in db_session.query(Word.word).join(SearchWords, Word.id == SearchWords.word_id).filter(SearchWords.session_id == p_session_id).all():
        ret.append(i[0])
    return ret

def get_or_create_user_session(user_id:int) -> Session:
    sess = db_session.query(Session).filter(Session.user_id == user_id).first()
    if sess == None:
    # не нашли сессию для этого пользователя
        sess = Session(user_id=user_id)
        db_session.add(sess)
        db_session.commit()
    return sess

def save_search_words(session_id:int, words:Iterable[int]) -> None:
    words_id = get_words_id(words)

    db_session.query(SearchWords).filter(SearchWords.session_id == session_id).delete()
    db_session.commit()

    # найти id всех книг, которые содержат все найденные слова
    for i in words_id:
        db_session.add(SearchWords(session_id=session_id, word_id=i))
    db_session.commit()