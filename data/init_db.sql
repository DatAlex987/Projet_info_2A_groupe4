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

### SOUNDECK
DROP TABLE IF EXISTS Sounddeck CASCADE ;
CREATE TABLE Sounddeck(
    id_sd INTEGER PRIMARY KEY,
    nom TEXT,
    description TEXT
);

#SCENE
DROP TABLE IF EXISTS Scene CASCADE ;
CREATE TABLE Scene (
    id_scene INTEGER PRIMARY KEY,
    nom TEXT,
    description TEXT,
    date_creation DATE
);

#SON
DROP TABLE IF EXISTS Scene CASCADE ;
CREATE TABLE Son (
    id_son INTEGER PRIMARY KEY,
    nom TEXT,
    description TEXT,
    duree INTEGER
);

#TAG
DROP TABLE IF EXISTS Tag CASCADE ;
CREATE TABLE Tag (
    nom_tag TEXT PRIMARY KEY
);

#User_Sounddeck
DROP TABLE IF EXISTS User_Sounddeck CASCADE ;
CREATE TABLE User_Sounddeck (
    id_user INTEGER,
    id_sd INTEGER,
    PRIMARY KEY (id_user, id_sd),
    FOREIGN KEY (id_user) REFERENCES User(id_user),
    FOREIGN KEY (id_sd) REFERENCES Sounddeck(id_sd)
);

#Sounddeck_Scene
DROP TABLE IF EXISTS Sounddeck_Scene CASCADE ;
CREATE TABLE Sounddeck_Scene(
    id_scene INTEGER,
    id_sd INTEGER,
    PRIMARY KEY (id_scene, id_sd),
    FOREIGN KEY (id_scene) REFERENCES Scene(id_scene),
    FOREIGN KEY (id_sd) REFERENCES Sounddeck(id_sd)
);

#Scene_Son
DROP TABLE IF EXISTS Scene_Son CASCADE ;
CREATE TABLE Scene_Son(
    id_scene INTEGER,
    id_son INTEGER,
    typ_param TEXT,
    PRIMARY KEY (id_scene, id_son),
    FOREIGN KEY (id_scene) REFERENCES Scene(id_scene),
    FOREIGN KEY (id_son) REFERENCES Son(id_son)
);

#Son_Tag
DROP TABLE IF EXISTS Son_Tag CASCADE ;
CREATE TABLE  Son_Tag (
    id_son INTEGER,
    nom_tag TEXT,
    PRIMARY KEY (id_son, nom_tag),
    FOREIGN KEY (id_son) REFERENCES Son(id_son),
    FOREIGN KEY (nom_tag) REFERENCES Tag(nom_tag)
);
