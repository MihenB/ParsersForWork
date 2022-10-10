-- CREATE TABLE news (
--   title text,
--   text text,
--   photo_path text,
--   tags text,
--   date text,
--   ID integer,
--   PRIMARY KEY (ID)
-- );
CREATE TABLE links_with_pages (
    id integer PRIMARY KEY AUTO_INCREMENT,
    link VARCHAR(512),
    page_num integer
);