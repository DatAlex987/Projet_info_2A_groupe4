-----------------------------------------------------
-- User
-----------------------------------------------------
DROP SCHEMA IF EXISTS SchemaTest CASCADE;
CREATE SCHEMA SchemaTest;

DROP TABLE IF EXISTS SchemaTest.Utilisateur CASCADE ;
CREATE TABLE SchemaTest.Utilisateur (
    id_user        SERIAL PRIMARY KEY,
    mdp_hashe      VARCHAR(256),
    date_naissance DATE,
    nom            VARCHAR(30),
    prenom         VARCHAR(30)

);

DROP TABLE IF EXISTS SchemaTest.Sounddeck CASCADE ;
CREATE TABLE SchemaTest.Sounddeck(
    id_sd SERIAL PRIMARY KEY,
    nom TEXT,
    description TEXT,
    date_creation DATE
);


DROP TABLE IF EXISTS SchemaTest.Scene CASCADE ;
CREATE TABLE SchemaTest.Scene (
    id_scene SERIAL PRIMARY KEY,
    nom TEXT,
    description TEXT,
    date_creation DATE
);

DROP TABLE IF EXISTS SchemaTest.Son CASCADE ;
CREATE TABLE SchemaTest.Son (
    id_freesound INTEGER PRIMARY KEY,
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
    id_user INTEGER,
    id_sd INTEGER,
    PRIMARY KEY (id_user, id_sd),
    FOREIGN KEY (id_user) REFERENCES Utilisateur(id_user),
    FOREIGN KEY (id_sd) REFERENCES Sounddeck(id_sd)
);


DROP TABLE IF EXISTS SchemaTest.Sounddeck_Scene CASCADE ;
CREATE TABLE SchemaTest.Sounddeck_Scene(
    id_scene INTEGER,
    id_sd INTEGER,
    PRIMARY KEY (id_scene, id_sd),
    FOREIGN KEY (id_scene) REFERENCES Scene(id_scene),
    FOREIGN KEY (id_sd) REFERENCES Sounddeck(id_sd)
);


DROP TABLE IF EXISTS SchemaTest.Scene_Son CASCADE ;
CREATE TABLE SchemaTest.Scene_Son(
    id_scene INTEGER,
    id_freesound INTEGER,
    type_param TEXT,
    PRIMARY KEY (id_scene, id_freesound),
    FOREIGN KEY (id_scene) REFERENCES Scene(id_scene),
    FOREIGN KEY (id_freesound) REFERENCES Son(id_freesound)
);


DROP TABLE IF EXISTS SchemaTest.Son_Tag CASCADE ;
CREATE TABLE  SchemaTest.Son_Tag(
    id_freesound INTEGER,
    nom_tag TEXT,
    PRIMARY KEY (id_freesound, nom_tag),
    FOREIGN KEY (id_freesound) REFERENCES Son(id_freesound),
    FOREIGN KEY (nom_tag) REFERENCES Tag(nom_tag)
);
