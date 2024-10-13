-----------------------------------------------------
-- User
-----------------------------------------------------
DROP SCHEMA IF EXISTS ProjetInfo CASCADE ; 
CREATE SCHEMA ProjetInfo ; 

DROP TABLE IF EXISTS ProjetInfo.Utilisateur CASCADE ;
CREATE TABLE ProjetInfo.Utilisateur (
    id_user      SERIAL PRIMARY KEY,
    pseudo       VARCHAR(30) UNIQUE,
    mdp_hashe    VARCHAR(256),
    age          INTEGER,
    nom          VARCHAR(30),
    prenom       VARCHAR(30)
);

DROP TABLE IF EXISTS ProjetInfo.Sounddeck CASCADE ;
CREATE TABLE ProjetInfo.Sounddeck(
    id_sd INTEGER PRIMARY KEY,
    nom TEXT,
    description TEXT
);


DROP TABLE IF EXISTS ProjetInfo.Scene CASCADE ;
CREATE TABLE ProjetInfo.Scene (
    id_scene INTEGER PRIMARY KEY,
    nom TEXT,
    description TEXT,
    date_creation DATE
);

DROP TABLE IF EXISTS ProjetInfo.Son CASCADE ;
CREATE TABLE ProjetInfo.Son (
    id_son INTEGER PRIMARY KEY,
    nom TEXT,
    description TEXT,
    duree INTEGER
);

DROP TABLE IF EXISTS ProjetInfo.Tag CASCADE ;
CREATE TABLE ProjetInfo.Tag(
    nom_tag TEXT PRIMARY KEY
);


DROP TABLE IF EXISTS ProjetInfo.User_Sounddeck CASCADE ;
CREATE TABLE ProjetInfo.User_Sounddeck (
    id_user INTEGER,
    id_sd INTEGER,
    PRIMARY KEY (id_user, id_sd),
    FOREIGN KEY (id_user) REFERENCES Utilisateur(id_user),
    FOREIGN KEY (id_sd) REFERENCES Sounddeck(id_sd)
);


DROP TABLE IF EXISTS ProjetInfo.Sounddeck_Scene CASCADE ;
CREATE TABLE ProjetInfo.Sounddeck_Scene(
    id_scene INTEGER,
    id_sd INTEGER,
    PRIMARY KEY (id_scene, id_sd),
    FOREIGN KEY (id_scene) REFERENCES Scene(id_scene),
    FOREIGN KEY (id_sd) REFERENCES Sounddeck(id_sd)
);


DROP TABLE IF EXISTS ProjetInfo.Scene_Son CASCADE ;
CREATE TABLE ProjetInfo.Scene_Son(
    id_scene INTEGER,
    id_son INTEGER,
    type_param TEXT,
    PRIMARY KEY (id_scene, id_son),
    FOREIGN KEY (id_scene) REFERENCES Scene(id_scene),
    FOREIGN KEY (id_son) REFERENCES Son(id_son)
);


DROP TABLE IF EXISTS ProjetInfo.Son_Tag CASCADE ;
CREATE TABLE  ProjetInfo.Son_Tag(
    id_son INTEGER,
    nom_tag TEXT,
    PRIMARY KEY (id_son, nom_tag),
    FOREIGN KEY (id_son) REFERENCES Son(id_son),
    FOREIGN KEY (nom_tag) REFERENCES Tag(nom_tag)
);
