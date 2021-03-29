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
    try:
        os.chdir(settings.LIBRARY_PATH)
        db_interface.rollback()
        ZIP_FILE="d.fb2-009373-367300.zip"
        z = zip_file.ZipFile(ZIP_FILE)
        b = z.get_book('110125.fb2')
        b.read_headers()
        b_m = db_interface.save_book(b)
        db_interface.commit()
    except Exception as e:
        logging.error(f"Book: {b}", exc_info=e)
    # with open("outfile2.txt","w") as f:
    #     print(b,file=f)
    # with open("outfile.txt","w") as f:
    #     for i in glob('*.zip'):
    #         try:
    #             z = zip_file.ZipFile(i)
    #             db_z = db_interface.save_zip_file(z)
    #             db_interface.commit()
    #             print(db_z)
    #             for b in z.get_book_list():
    #                 b.read_headers()
    #                 b_m = db_interface.save_book(b)
    #                 db_interface.commit()
    #         except Exception as e:
    #             logging.error(f"Book: {b}", exc_info=e)



if __name__ == '__main__':
    main()