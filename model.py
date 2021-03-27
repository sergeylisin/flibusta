from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relation, relationship
from sqlalchemy.sql.schema import FetchedValue, ForeignKeyConstraint, Index, PrimaryKeyConstraint
from db import Base, engine


class ZipFile(Base):
    __tablename__="zipfile"
    zip_name = Column(name="zip_name",primary_key=True,type_=String)

    def __repr__(self):
        return f"ZipFile: {self.zip_name}"

class Book(Base):
    __tablename__ = "books"
    id = Column(name="id",type_=Integer,autoincrement=True,primary_key=False,server_default=FetchedValue())
    zip_name = Column("zip_name",type_=String, primary_key=True)
    book_name = Column("book_name",type_=String,primary_key=True)
    annotation = Column(name="annotation",type_=Text)
    authors = Column("authors",type_=Text)
    language = Column("language",type_=String)
    title = Column("title",type_=Text)

    def __repr__(self):
        return f"Book: zip_name={self.zip_name} book_name={self.book_name}"

class Word(Base):
    __tablename__="words"
    id = Column("id",type_=Integer,primary_key=True, autoincrement=True, server_default=FetchedValue())
    word = Column("word",type_=String(255))
    cnt = Column("cnt", type_=Integer, default=1)
    word_i1 = Index("word")

    def __repr__(self):
        return f"Word: {self.word}"
    
class BookWord(Base):
    __tablename__="book_words"
    book_id = Column("book_id",Integer,primary_key=True)
    word_id = Column("word_id",Integer, primary_key=True)

    def __repr__(self):
        return f"book_id={self.book_id} word_id={self.word_id}"

class Session(Base):
    __tablename__="session"
    id = Column("id",Integer, primary_key=True, autoincrement=True,server_default=FetchedValue())
    start_date = Column("start_date",DateTime,primary_key=True,server_default=FetchedValue())

class WordTemp(Base):
    __tablename__="word_temp"
    session_id = Column("session_id",Integer)
    word_id = Column("word_id",Integer)
    word_temp_pk = PrimaryKeyConstraint(session_id,word_id)

