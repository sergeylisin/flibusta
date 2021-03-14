import book
import zip_file

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.sql.schema import FetchedValue, Index, PrimaryKeyConstraint
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

class Word(Base):
    __tablename__="words"
    id = Column("id",primary_key=True, autoincrement=True, server_default=FetchedValue())
    word = Column("word",type_=String(255))
    cnt = Column("cnt", type_=Integer)
    word_i1 = Index("word")
    

