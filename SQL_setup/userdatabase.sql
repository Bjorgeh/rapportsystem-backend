CREATE DATABASE users;

USE users;

-- Setter opp brukertabellen
CREATE TABLE user_info(
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(50) UNIQUE,
    accountType VARCHAR(255),
    databaseName VARCHAR(255) UNIQUE,
    userPass VARCHAR(255), 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Oppretter en ny tabell for JWT-tokens
CREATE TABLE tokens (
    token_id VARCHAR(767) PRIMARY KEY,
    user_id INT,
    expiration DATETIME DEFAULT (CURRENT_TIMESTAMP + INTERVAL 30 MINUTE),
    revoked BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES user_info(id)
);

-- Setter opp aktivitetstabellen
CREATE TABLE user_activity(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    ip_address VARCHAR(50),
    user_agent VARCHAR(255),
    operating_system VARCHAR(255),  
    activity_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_info(id)
);

