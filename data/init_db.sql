-----------------------------------------------------
-- User
-----------------------------------------------------
DROP TABLE IF EXISTS Utilisateur CASCADE ;
CREATE TABLE Utilisateur (
    id_user      SERIAL PRIMARY KEY,
    pseudo       VARCHAR(30) UNIQUE,
    mdp_hashe    VARCHAR(256),
    age          INTEGER,
    nom          VARCHAR(30),
    prenom       VARCHAR(30)
);

DROP TABLE IF EXISTS Sounddeck CASCADE ;
CREATE TABLE Sounddeck(
    id_sd INTEGER PRIMARY KEY,
    nom TEXT,
    description TEXT
);


DROP TABLE IF EXISTS Scene CASCADE ;
CREATE TABLE Scene (
    id_scene INTEGER PRIMARY KEY,
    nom TEXT,
    description TEXT,
    date_creation DATE
);

DROP TABLE IF EXISTS Son CASCADE ;
CREATE TABLE Son (
    id_son INTEGER PRIMARY KEY,
    nom TEXT,
    description TEXT,
    duree INTEGER
);

DROP TABLE IF EXISTS Tag CASCADE ;
CREATE TABLE Tag(
    nom_tag TEXT PRIMARY KEY
);


DROP TABLE IF EXISTS User_Sounddeck CASCADE ;
CREATE TABLE User_Sounddeck (
    id_user INTEGER,
    id_sd INTEGER,
    PRIMARY KEY (id_user, id_sd),
    FOREIGN KEY (id_user) REFERENCES Utilisateur(id_user),
    FOREIGN KEY (id_sd) REFERENCES Sounddeck(id_sd)
);


DROP TABLE IF EXISTS Sounddeck_Scene CASCADE ;
CREATE TABLE Sounddeck_Scene(
    id_scene INTEGER,
    id_sd INTEGER,
    PRIMARY KEY (id_scene, id_sd),
    FOREIGN KEY (id_scene) REFERENCES Scene(id_scene),
    FOREIGN KEY (id_sd) REFERENCES Sounddeck(id_sd)
);


DROP TABLE IF EXISTS Scene_Son CASCADE ;
CREATE TABLE Scene_Son(
    id_scene INTEGER,
    id_son INTEGER,
    type_param TEXT,
    PRIMARY KEY (id_scene, id_son),
    FOREIGN KEY (id_scene) REFERENCES Scene(id_scene),
    FOREIGN KEY (id_son) REFERENCES Son(id_son)
);


DROP TABLE IF EXISTS Son_Tag CASCADE ;
CREATE TABLE  Son_Tag(
    id_son INTEGER,
    nom_tag TEXT,
    PRIMARY KEY (id_son, nom_tag),
    FOREIGN KEY (id_son) REFERENCES Son(id_son),
    FOREIGN KEY (nom_tag) REFERENCES Tag(nom_tag)
);
