import book as b
from model import SearchResult, SearchWords, Session, BookWord, Book
import tokenizer
import db_interface
from typing import List
from db import db_session
from sqlalchemy import func, and_


class SearchSession:
    def __init__(self, p_user_id: int):
        # проверяем, есть ли сессия для этого пользователя
        # если есть - то загружаем ее, и список ранее найденых книг
        self.sess = db_session.query(Session).filter(Session.user_id == p_user_id).first()
        if self.sess == None:
            # не нашли сессию для этого пользователя
            self.sess = Session(user_id=p_user_id)
            db_session.add(self.sess)
            db_session.commit()
        self.session_id = self.sess.id
        self.search_result = []

    def search(self, text: str):
        language = tokenizer.guess_language(text)
        words = tokenizer.word_tokenize(text, language)
        words_id = db_interface.get_words_id(words)

        # очищаем список слов, использованный при предыдущем поиске
        db_session.query(SearchWords).filter(SearchWords.session_id == self.sess.id).delete()
        db_session.commit()

        # найти id всех книг, которые содержат все найденные слова
        for i in words_id:
            db_session.add(SearchWords(session_id=self.session_id, word_id=i))
        db_session.commit()
        q = db_session.query(BookWord.book_id).\
            join(SearchWords, and_(SearchWords.session_id == self.session_id, SearchWords.word_id == BookWord.word_id)).\
            group_by(BookWord.book_id).\
            having(func.count(BookWord.word_id) == db_session.query(func.count(SearchWords.word_id.distinct())).
                   filter(SearchWords.session_id == self.session_id)
                   )
        self.search_result.clear()

        # очищаем результат предыдущего поиска
        db_session.query(SearchResult).filter(SearchResult.session_id == self.sess.id).delete()
        db_session.commit()

        for i in q.all():
            book = db_session.query(Book).filter(Book.id == i[0]).first()
            self.search_result.append(
                b.Book(zip_file=book.zip_name, book_name=book.book_name,
                       annotation=book.annotation, authors=book.authors,
                       title=book.title, genre=book.genre)
            )
            db_session.add(SearchResult(session_id = self.sess.id,book_id = book.id))
        db_session.commit()
