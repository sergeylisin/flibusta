import book
import zip_file

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.sql.schema import FetchedValue, PrimaryKeyConstraint
from db import Base, engine

class ZipFile(Base):
    def __init__(self,zip_file: zip_file.ZipFile):
        self.zip_name = zip_file.zip_name
    __tablename__="zipfile"
    zip_name = Column(name="zip_name",primary_key=True,type_=String)

class Book(Base):
    def __init__(self,book: book.Book):
        self.zip_name = book.zip_file.zip_name
        self.book_name = book.book_name
        self.language = book.lang
        self.annotation = book.annotation
        self.genre = book.genre
        self.authors = book.authors
        self.title = book.title
    __tablename__ = "book"
    id = Column(name="id",type_=Integer,autoincrement=True,primary_key=False,server_default=FetchedValue())
    zip_name = Column("zip_name",type_=String, primary_key=True)
    book_name = Column("book_name",type_=String,primary_key=True)
    annotation = Column(name="annotation",type_=Text)
    authors = Column("authors",type_=Text)
    language = Column("language",type_=String)
    title = Column("title",type_=Text)

