CREATE TABLE users (
    id INT AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    login VARCHAR(125) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE blogs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    deleted BOOLEAN,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE posts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE blogs_posts (
    blog_id INT,
    post_id INT,
    PRIMARY KEY (blog_id, post_id),
    FOREIGN KEY (blog_id) REFERENCES blogs(id),
    FOREIGN KEY (post_id) REFERENCES posts(id)
);

CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    user_id INT NOT NULL,
    parent_post_id INT,
    parent_comment_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (parent_post_id) REFERENCES posts(id),
    FOREIGN KEY (parent_comment_id) REFERENCES comments(id)
);


INSERT INTO users (first_name, last_name, login, password)
    VALUES ('Дмитрий', 'Гал', 'Gal', 'pass');

INSERT INTO users (first_name, last_name, login, password)
    VALUES ('Вася', 'Пупкин', 'Vasaya', 'passwd');
