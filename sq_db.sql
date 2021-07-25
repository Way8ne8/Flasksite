create table if not exists mainmenu (
id integer primary key autoincrement,
title text not null,
url text not null
);

CREATE TABLE IF NOT EXISTS posts (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
text text NOT NULL,
time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS contact (
id integer PRIMARY KEY AUTOINCREMENT,
username NOT NULL,
email NOT NULL,
message NOT NULL
);