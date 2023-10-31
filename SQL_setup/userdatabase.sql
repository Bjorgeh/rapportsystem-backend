#CREATE DATABASE users;

USE users;

CREATE TABLE users_info(
	email VARCHAR(50) PRIMARY KEY,
    databaseName VARCHAR(255),
    userPass VARCHAR(255)
);

