CREATE TABLE users (
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    email VARCHAR(255),
    password VARCHAR(255),
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

INSERT INTO users(email, password, role) VALUES
('admin@gmail.com', '2a9fba131908e03e95050deeb413df95997e8a20ad6d623c1d16d6d34533689e', 'admin'), # seedpassword1
('basic@gmail.com', '4eea0b3bc0bdbb7a3ad0b14cb6adcf489cd0b13ad76e74a08d8dee126b8f1b01', 'basic'); # seedpassword2