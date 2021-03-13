from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from db import Base, engine

class ZipFile(Base):
    __tablename__="zipfile"
    zip_name = Column(name="zip_name",primary_key=True,type_=String)

class Book(Base)    :
    __tablename__ = "book"
    id = Column(name="id",type_=Integer,autoincrement=True,primary_key=False)
    zip_name = Column("zip_name",type_=String)
    book_name = Column("book_name",type_=String)
    annotation = Column(name="annotation",type_=Text)
    authors = Column("authors",type_=Text)
    language = Column("language",type_=String)
    title = Column("title",type_=Text)
    book_pk = PrimaryKeyConstraint(Column("zip_name"),Column("book_name"))

