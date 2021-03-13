import settings
import zip_file
from glob import glob
from itertools import islice
import os
import logging
from db import Base, db_session, engine

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
            db_session.merge(z)
            db_session.commit()
            for b in z.get_book_list():
                b.read_headers()
                db_session.merge(b)
                db_session.commit()
#                print(b,file=f)


if __name__ == '__main__':
    main()