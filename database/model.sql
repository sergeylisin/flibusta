drop table book_words;
drop table session_search_words;
drop table search_result;
drop table words;
drop table books;
drop table zipfile;
drop table session;


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

CREATE unique INDEX word_i1 ON words (word);

CREATE TABLE books (
  id serial,
  book_name varchar(255) NOT NULL,
  zip_name varchar(255) NOT NULL,
  annotation text,
  authors text ,
  title text,
  genre varchar(255),
  language varchar(255) ,
  PRIMARY KEY (zip_name,book_name),
  CONSTRAINT books_zip_name_zipfile_zip_name_fk FOREIGN KEY (zip_name) REFERENCES zipfile (zip_name),
  constraint books_uniq_id unique(id)
);

CREATE TABLE book_words (
  book_id integer NOT NULL,
  word_id integer NOT NULL,
  CONSTRAINT book_words_book_id_book_id_foreign FOREIGN KEY (book_id) REFERENCES books (id),
  CONSTRAINT book_words_word_id_words_id_foreign FOREIGN KEY (word_id) REFERENCES words (id),
  primary key(book_id,word_id)
);

create index book_words_word_id on book_words(word_id);

create index book_words_book_id on book_words(book_id);

create table session (
  id serial primary key,
  start_date date default now(),
  user_id integer
);

create table session_search_words (
  session_id integer,
  word_id integer,
  CONSTRAINT word_srch_word_id_words_id_foreign FOREIGN KEY (word_id) REFERENCES words (id),
  CONSTRAINT word_srch_session_id_fk FOREIGN KEY (session_id) REFERENCES session (id)
);

create index sess_srch_words_sess_id on session_search_words(session_id);

create table search_result (
  session_id integer ,
  book_id integer,
  constraint srch_rslt_sess_id foreign key(session_id) references session(id),
  constraint srch_rslt_book_id foreign key(book_id) references books(id),
  constraint srch_rslt_pk primary key(session_id,book_id)
);

create index srch_rslt_i1 on search_result(session_id);



