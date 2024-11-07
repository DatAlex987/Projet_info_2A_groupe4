-----------------------------------------------------
-- User
-----------------------------------------------------
DROP SCHEMA IF EXISTS SchemaTest CASCADE;
CREATE SCHEMA SchemaTest;

DROP TABLE IF EXISTS SchemaTest.Utilisateur CASCADE ;
CREATE TABLE SchemaTest.Utilisateur (
    id_user        VARCHAR(30) PRIMARY KEY,
    mdp_hashe      VARCHAR(256),
    date_naissance DATE,
    nom            VARCHAR(30),
    prenom         VARCHAR(30),
    pseudo         VARCHAR(30) UNIQUE

);

DROP TABLE IF EXISTS SchemaTest.Sounddeck CASCADE ;
CREATE TABLE SchemaTest.Sounddeck(
    id_sd VARCHAR(30) PRIMARY KEY,
    nom TEXT,
    description TEXT,
    date_creation DATE
);


DROP TABLE IF EXISTS SchemaTest.Scene CASCADE ;
CREATE TABLE SchemaTest.Scene (
    id_scene VARCHAR(30) PRIMARY KEY,
    nom TEXT,
    description TEXT,
    date_creation DATE
);

DROP TABLE IF EXISTS SchemaTest.Son CASCADE ;
CREATE TABLE SchemaTest.Son (
    id_freesound VARCHAR(30) PRIMARY KEY,
    nom TEXT,
    description TEXT,
    duree TIME
);

DROP TABLE IF EXISTS SchemaTest.Tag CASCADE ;
CREATE TABLE SchemaTest.Tag(
    nom_tag TEXT PRIMARY KEY
);


DROP TABLE IF EXISTS SchemaTest.User_Sounddeck CASCADE ;
CREATE TABLE SchemaTest.User_Sounddeck (
    id_user VARCHAR(30),
    id_sd VARCHAR(30),
    PRIMARY KEY (id_user, id_sd),
    FOREIGN KEY (id_user) REFERENCES SchemaTest.Utilisateur(id_user) ON DELETE CASCADE,
    FOREIGN KEY (id_sd) REFERENCES SchemaTest.Sounddeck(id_sd) ON DELETE CASCADE
);


DROP TABLE IF EXISTS SchemaTest.Sounddeck_Scene CASCADE ;
CREATE TABLE SchemaTest.Sounddeck_Scene(
    id_scene VARCHAR(30),
    id_sd VARCHAR(30),
    PRIMARY KEY (id_scene, id_sd),
    FOREIGN KEY (id_scene) REFERENCES SchemaTest.Scene(id_scene) ON DELETE CASCADE,
    FOREIGN KEY (id_sd) REFERENCES SchemaTest.Sounddeck(id_sd) ON DELETE CASCADE
);


DROP TABLE IF EXISTS SchemaTest.Scene_Son CASCADE ;
CREATE TABLE SchemaTest.Scene_Son(
    id_scene VARCHAR(30),
    id_freesound VARCHAR(30),
    param1 TEXT,
    param2 TEXT,
    type VARCHAR(30),
    PRIMARY KEY (id_scene, id_freesound, type),
    FOREIGN KEY (id_scene) REFERENCES SchemaTest.Scene(id_scene) ON DELETE CASCADE,
    FOREIGN KEY (id_freesound) REFERENCES SchemaTest.Son(id_freesound) ON DELETE CASCADE
);


DROP TABLE IF EXISTS SchemaTest.Son_Tag CASCADE ;
CREATE TABLE  SchemaTest.Son_Tag(
    id_freesound VARCHAR(30),
    nom_tag TEXT,
    PRIMARY KEY (id_freesound, nom_tag),
    FOREIGN KEY (id_freesound) REFERENCES SchemaTest.Son(id_freesound) ON DELETE CASCADE,
    FOREIGN KEY (nom_tag) REFERENCES SchemaTest.Tag(nom_tag) ON DELETE CASCADE
);
