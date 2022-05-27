CREATE TABLE users (
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    email VARCHAR(255),
    role VARCHAR(255),
    PRIMARY KEY (id)
);

CREATE TABLE logs (
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    user_id MEDIUMINT NOT NULL,
    url TEXT NOT NULL,
    headers MEDIUMTEXT NOT NULL,
    request JSON NOT NULL,
    response JSON NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO users(email, role) VALUES
('admin@gmail.com', 'admin'),
('basic@gmail.com', 'basic');