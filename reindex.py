import settings
from glob import glob
import os
import logging
import db_interface
import zip_file


logging.basicConfig(filename="flibusta.log")
#logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)



def main():
    os.chdir(settings.LIBRARY_PATH)

    for i in glob('*.zip'):
        z = zip_file.ZipFile(i)
        db_z = db_interface.save_zip_file(z)
        db_interface.commit()
        for b in z.get_book_list():
            try:
                b.read_headers()
                b_m = db_interface.save_book(b)
                db_interface.commit()
            except Exception as e:
                logging.error(f"Book: {b}", exc_info=e)
                db_interface.rollback()



if __name__ == '__main__':
    main()