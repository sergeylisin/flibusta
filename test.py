from search import SearchSession
import settings
from glob import glob
import os
import logging
from model import ZipFile, Book, Session
import db_interface
import zip_file




logging.basicConfig(filename="flibusta.log")
#logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)



def main():
    text = "пылающий остров"
    s = SearchSession()
    s.search(text)
    print(s.search_result)
    



if __name__ == '__main__':
    main()