from search import SearchSession
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
    s = SearchSession(p_user_id=1)
    s.search(text)
    pprint(s.search_result)
    



if __name__ == '__main__':
    main()