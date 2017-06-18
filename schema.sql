#drop table if exists Users;
	create table users (
    id integer primary key autoincrement,
    username text not null,
    password text not null
);
	create table rooms (
	id integer primary key autoincrement,
	roomname text not null)