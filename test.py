from search import SearchSession, get_session
import settings
from glob import glob
import os
import logging
from model import ZipFile, Book, Session
import db_interface
import zip_file
from pprint import pprint




logging.basicConfig(filename="flibusta.log")
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)



def main():
    text = "пылающий остров"
    s = get_session(1)
    s.search(text)
    pprint(s.search_result)
    



if __name__ == '__main__':
    main()