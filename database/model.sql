drop table book_words;
drop table words;
drop table book;
drop table zipfile;

CREATE TABLE zipfile (
  zip_name varchar(255) NOT NULL,
  PRIMARY KEY (zip_name)
);

CREATE TABLE words (
  id serial NOT NULL,
  word varchar(255) DEFAULT NULL,
  cnt integer DEFAULT NULL,
  PRIMARY KEY (id)
);
CREATE INDEX index_1 ON words (word);

CREATE TABLE book (
  id serial,
  book_name varchar(255) NOT NULL,
  zip_name varchar(255) NOT NULL,
  annotation text,
  authors text ,
  title text,
  language varchar(255) ,
  PRIMARY KEY (zip_name,book_name),
  CONSTRAINT book_zip_name_zipfile_zip_name_fk FOREIGN KEY (zip_name) REFERENCES zipfile (zip_name),
  constraint uniq_id unique(id)
);

CREATE TABLE book_words (
  book_id integer NOT NULL,
  word_id integer NOT NULL,
  CONSTRAINT book_words_book_id_book_id_foreign FOREIGN KEY (book_id) REFERENCES book (id),
  CONSTRAINT book_words_word_id_words_id_foreign FOREIGN KEY (word_id) REFERENCES words (id)
);


