CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (username, email, password) VALUES
    ('alice', 'alice@example.com', 'password123'),
    ('bob', 'bob@example.com', 'password456');