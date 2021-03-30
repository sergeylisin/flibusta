import zip_file
from typing import Set
import xmltodict
from typing import Set
import tokenizer



NAMESPACES = {'fb2': 'http://www.gribuser.ru/xml/fictionbook/2.0'}


def dict_to_str(v, exclude: Set = set([])):
    ret = ""
    if isinstance(v, str):
        ret = v.replace("\x0a", "").replace("\x09", "").replace("\x0d", "")
    elif isinstance(v, list):
        ret = " ".join(map(lambda x: dict_to_str(x, exclude), v))
    elif isinstance(v, dict):
        ret = " ".join(map(lambda x: dict_to_str(x, exclude),
                           map(lambda x: x[1], filter(
                               lambda y: y[0] not in exclude, v.items()))
                           ))
    return ret


def guess_book_language(book):
    ret_lang = tokenizer.LANG_MAP.get(book.lang)
    if tokenizer.LANG_MAP.get(book.lang) == None:
        if book.annotation != " ":
            ret_lang = tokenizer.guess_language(
                book.title + " " + book.authors + " " + book.annotation)
        else:
            ret_lang = tokenizer.guess_language(
                book.title + " " + book.authors)
    return ret_lang


class Book:
    def __init__(self,**kwargs ):
        self.words = None
        self.zip_file = zip_file.ZipFile(kwargs.get('zip_file'))
        self.book_name = kwargs.get('book_name') or ""
        self.annotation = kwargs.get('annotation') or ""
        self.title = kwargs.get('title') or ""
        self.genre = kwargs.get('genre') or ""
        self.lang = kwargs.get('lang') or ""
        self.authors = kwargs.get('authors') or ""
        self.__get_words()


    def open(self):
        return self.zip_file.open(self.book_name)

    def read_headers(self):
        with self.open() as b:
            book = xmltodict.parse(b)
            book_description = book["FictionBook"]["description"]["title-info"]
            self.title = (dict_to_str(
                book_description.get('book-title')) or " ")
            self.annotation = (dict_to_str(
                book_description.get("annotation")) or " ")
            self.annotation = self.annotation.replace(
                "\n", "").replace("\r", "")
            self.authors = (dict_to_str(
                book_description.get("author"), set(["id"])) or " ")
            self.authors = self.authors.replace("\n", "").replace("\r", "")
            self.lang = book_description.get("lang")
            self.lang = guess_book_language(self)
            self.genre = book_description.get("genre")
            self.__get_words()

    def __repr__(self):
        return f"zip: {self.zip_file.__repr__()} book:{self.book_name} language:{self.lang} authors:{self.authors} title:{self.title} "

    def __get_words(self):
        text = self.authors + " " + self.title + " " + self.annotation
        self.words = tokenizer.word_tokenize(text, self.lang)
        if self.words == None:
            self.words = set()
