import settings
import book
import zipfile

class ZipFile:
    def __init__(self,zip_name):
        self.zip_name = zip_name

    def get_book_list(self):
        with zipfile.ZipFile(settings.LIBRARY_PATH + '/' + self.zip_name) as z:
            for b in z.namelist():
                yield book.Book(self, b)

    def get_book(self,book_name):
        self.__zip_file = zipfile.ZipFile(settings.LIBRARY_PATH + '/' + self.zip_name)
        return book.Book(self,book_name)

    def __enter__(self):
        self.__zip_file = zipfile.ZipFile(settings.LIBRARY_PATH + '/' + self.zip_name)
        return self
    
    def __exit__(self,type,value,traceback):
        self.close()
        return False

    def open(self,book_name):
        self.__zip_file = zipfile.ZipFile(settings.LIBRARY_PATH + '/' + self.zip_name)
        return self.__zip_file.open(book_name,'r')

    def close(self):
        self.__zip_file.close()
    
    def get_name(self):
        return self.zip_name
 
    def __repr__(self):
        return str(self.zip_name)

