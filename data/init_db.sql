-----------------------------------------------------
-- User
-----------------------------------------------------
DROP SCHEMA IF EXISTS ProjetInfo CASCADE;
CREATE SCHEMA ProjetInfo;

DROP TABLE IF EXISTS ProjetInfo.Utilisateur CASCADE ;
CREATE TABLE ProjetInfo.Utilisateur (
    id_user        VARCHAR(30) PRIMARY KEY,
    mdp_hashe      VARCHAR(256),
    date_naissance DATE,
    nom            VARCHAR(30),
    prenom         VARCHAR(30)

);

DROP TABLE IF EXISTS ProjetInfo.Sounddeck CASCADE ;
CREATE TABLE ProjetInfo.Sounddeck(
    id_sd VARCHAR(30) PRIMARY KEY,
    nom TEXT,
    description TEXT,
    date_creation DATE
);


DROP TABLE IF EXISTS ProjetInfo.Scene CASCADE ;
CREATE TABLE ProjetInfo.Scene (
    id_scene VARCHAR(30) PRIMARY KEY,
    nom TEXT,
    description TEXT,
    date_creation DATE
);

DROP TABLE IF EXISTS ProjetInfo.Son CASCADE ;
CREATE TABLE ProjetInfo.Son (
    id_freesound VARCHAR(30) PRIMARY KEY,
    nom TEXT,
    description TEXT,
    duree TIME
);

DROP TABLE IF EXISTS ProjetInfo.Tag CASCADE ;
CREATE TABLE ProjetInfo.Tag(
    nom_tag TEXT PRIMARY KEY
);


DROP TABLE IF EXISTS ProjetInfo.User_Sounddeck CASCADE ;
CREATE TABLE ProjetInfo.User_Sounddeck (
    id_user VARCHAR(30),
    id_sd VARCHAR(30),
    PRIMARY KEY (id_user, id_sd),
    FOREIGN KEY (id_user) REFERENCES Utilisateur(id_user) ON DELETE CASCADE,
    FOREIGN KEY (id_sd) REFERENCES Sounddeck(id_sd) ON DELETE CASCADE
);


DROP TABLE IF EXISTS ProjetInfo.Sounddeck_Scene CASCADE ;
CREATE TABLE ProjetInfo.Sounddeck_Scene(
    id_scene VARCHAR(30),
    id_sd VARCHAR(30),
    PRIMARY KEY (id_scene, id_sd),
    FOREIGN KEY (id_scene) REFERENCES Scene(id_scene) ON DELETE CASCADE,
    FOREIGN KEY (id_sd) REFERENCES Sounddeck(id_sd) ON DELETE CASCADE
);


DROP TABLE IF EXISTS ProjetInfo.Scene_Son CASCADE ;
CREATE TABLE ProjetInfo.Scene_Son(
    id_scene VARCHAR(30),
    id_freesound VARCHAR(30),
    type_param TEXT,
    PRIMARY KEY (id_scene, id_freesound),
    FOREIGN KEY (id_scene) REFERENCES Scene(id_scene) ON DELETE CASCADE,
    FOREIGN KEY (id_freesound) REFERENCES Son(id_freesound) ON DELETE CASCADE
);


DROP TABLE IF EXISTS ProjetInfo.Son_Tag CASCADE ;
CREATE TABLE  ProjetInfo.Son_Tag(
    id_freesound VARCHAR(30),
    nom_tag TEXT,
    PRIMARY KEY (id_freesound, nom_tag),
    FOREIGN KEY (id_freesound) REFERENCES Son(id_freesound) ON DELETE CASCADE,
    FOREIGN KEY (nom_tag) REFERENCES Tag(nom_tag) ON DELETE CASCADE
);
