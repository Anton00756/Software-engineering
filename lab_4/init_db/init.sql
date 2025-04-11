CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    login VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE INDEX IF NOT EXISTS user_index ON users(login, surname, name);

CREATE TABLE IF NOT EXISTS group_chats (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS group_chat_members (
    group_chat_id INT REFERENCES group_chats(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (group_chat_id, user_id)
);

CREATE TABLE IF NOT EXISTS private_chats (
    id SERIAL PRIMARY KEY,
    user1 INT REFERENCES users(id) ON DELETE CASCADE,
    user2 INT REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);