from model import WordTemp, Session, BookWord, Book
import tokenizer
import db_interface
from typing import Optional,List
from db import db_session
from sqlalchemy import func, and_


class SearchSession:
    def __init__(self):
        sess = Session()
        db_session.add(sess)
#        db_session.query(Session).filter(Session.start_date < func.now()).delete()
        db_session.commit()
        self.session_id = sess.id

    def search(self,text:str) :
        language = tokenizer.guess_language(text)
        words = tokenizer.word_tokenize(text,language)
        words_id = db_interface.get_words_id(words)
        ret_books = []
# найти id всех книг, которые содержат все найденные слова
        for i in words_id:
            db_session.add(WordTemp(session_id = self.session_id, word_id = i))
        db_session.commit()
        q = db_session.query(BookWord.book_id).\
            join(WordTemp,and_(WordTemp.session_id == self.session_id , WordTemp.word_id == BookWord.word_id)).\
            group_by(BookWord.book_id).\
            having(func.count(BookWord.word_id) == db_session.query(func.count(WordTemp.word_id.distinct())).\
                filter(WordTemp.session_id == self.session_id)\
            )
        for i in q.all():
            book = db_session.query(Book).filter(Book.id == i[0]).first()
            ret_books.append(book)
        return ret_books
    #     .as_scalar() 
    # return q
    
        
            
    