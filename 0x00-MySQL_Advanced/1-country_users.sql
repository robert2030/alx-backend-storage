-- Create A user with following attributes;
-- id
-- email
-- name
-- country (ENUM)

CREATE TABLE IF NOT EXISTS users(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
email VARCHAR(255) UNIQUE NOT NULL,
name VARCHAR(255),
country ENUM ("US", "CO", "TN") NOT NULL DEFAULT "US");
