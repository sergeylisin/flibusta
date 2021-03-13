from typing import Set
import xmltodict
import logging
from typing import Set


NAMESPACES = {'fb2': 'http://www.gribuser.ru/xml/fictionbook/2.0'}


def dict_to_str(v, exclude: Set = set([])):
    ret = ""
    if isinstance(v, str):
        ret = v.replace("\x0a","").replace("\x09","").replace("\x0d","")
    elif isinstance(v, list):
        ret = " ".join(map(lambda x: dict_to_str(x, exclude), v))
    elif isinstance(v, dict):
        ret = " ".join(map(lambda x: dict_to_str(x, exclude),
                           map(lambda x: x[1], filter(
                               lambda y: y[0] not in exclude, v.items()))
                           ))
    return ret

class Book:
    def __init__(self, zip_file, book_name):
        self.__book_name = book_name
        self.__zip_file = zip_file
        self.authors = None
        self.title = None
        self.annotation = None
        self.genre = None
        self.lang = None
        self.words = None

    def open(self):
        return self.__zip_file.open(self.__book_name)

    def read_headers(self):
        with self.open() as b:
            try:
                book = xmltodict.parse(b)
                book_description = book["FictionBook"]["description"]["title-info"]
                self.title = (dict_to_str(book_description.get('book-title')) or " ")
                self.annotation = (dict_to_str(
                    book_description.get("annotation")) or " ")
                self.annotation = self.annotation.replace("\n","").replace("\r","")
                self.authors = (dict_to_str(
                    book_description.get("author"),set(["id"])) or " ")
                self.authors = self.authors.replace("\n","").replace("\r","")
                self.lang = book_description.get("lang")
                

            except Exception as e:
                logging.error(
                    f"Zip: {self.__zip_file.get_name()} Book: {self.__book_name}", exc_info=e)

    def __repr__(self):
        return f"zip: {self.__zip_file.__str__()} book:{self.__book_name} language:{self.lang} authors:{self.authors} title:{self.title} annotation:{self.annotation}"

