#CREATE DATABASE users;

USE users;
-- sets up user table
CREATE TABLE user_info(
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(50) UNIQUE,
    accountType VARCHAR(255),
    userPass VARCHAR(255),  -- Hashed pass
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- sets up session table
CREATE TABLE user_session(
    session_id VARCHAR(255) PRIMARY KEY,
    user_id INT,
    data TEXT, 
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    expiration DATETIME DEFAULT (CURRENT_TIMESTAMP + INTERVAL 30 MINUTE),
    FOREIGN KEY (user_id) REFERENCES user_info(id)
);
