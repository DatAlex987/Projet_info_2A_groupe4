-----------------------------------------------------
-- User
-----------------------------------------------------
DROP TABLE IF EXISTS User CASCADE ;
CREATE TABLE User(
    id_user    SERIAL PRIMARY KEY,
    pseudo       VARCHAR(30) UNIQUE,
    mdp          VARCHAR(256),
    age          INTEGER,
    mail         VARCHAR(50)
);
