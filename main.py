import settings
import zip_file
from glob import glob
import os
import logging
from db import Base, db_session, engine
import model

logging.basicConfig(filename="flibusta.log")



def main():
    os.chdir(settings.LIBRARY_PATH)
    # ZIP_FILE="f.fb2-386287-389890.zip"
    # z = zip_file.ZipFile(ZIP_FILE)
    # b = z.get_book("387888.fb2")
    # b.read_headers()
    # with open("outfile2.txt","w") as f:
    #     print(b,file=f)
    with open("outfile.txt","w") as f:
        for i in glob('*.zip'):
            z = zip_file.ZipFile(i)
            z_m = model.ZipFile(z)
            db_session.merge(z_m)
            db_session.commit()
            for b in z.get_book_list():
                b.read_headers()
                b_m = model.Book(b)
                db_session.merge(b_m)
                db_session.commit()
                print(b,file=f)


if __name__ == '__main__':
    main()