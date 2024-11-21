# tests manuels DAO, instancié tous les users, sd, scène, son, tag possibles...

from dao.db_connection import DBConnection
from business_object.user import User
from business_object.personne import Personne
from business_object.scene import Scene
from business_object.sd import SD
import datetime
from utils.reset_database import ResetDatabase
from dao.user_dao import UserDAO
from dao.sd_dao import SDDAO
from dao.scene_dao import SceneDAO
from dao.son_dao import SonDAO
from dao.tag_dao import TagDAO
from business_object.son import Son
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_manuel import Son_Manuel
from business_object.son_continu import Son_Continu
from service.session import Session
from service.freesound import Freesound
from service.son_service import SonService
import hashlib
from src.service.scene_service import SceneService
import os
import re
from datetime import timedelta
import pygame
import sys


"""Son_c = Son_Continu(
    nom="Musique douce",
    description="Musique douce au piano",
    duree=datetime.timedelta(minutes=15),
    id_freesound="747222",
    id_son="e6uKHU85",
    tags=["piano", "calm", "soft"],
)

son_a = Son_Aleatoire(
    nom="Musique douce",
    description="Musique douce au piano",
    duree=datetime.timedelta(minutes=15),
    id_freesound="265180",
    id_son="e6uKHU85",
    tags=["piano", "calm", "soft"],
    cooldown_min=6,
    cooldown_max=12,
)


Son_c2 = Son_Continu(
    nom="Musique douce",
    description="Musique douce au piano",
    duree=datetime.timedelta(minutes=15),
    id_freesound="227558",
    id_son="e6uKHU85",
    tags=["piano", "calm", "soft"],
)


def son_aleatoire2_kwargs():
    return {
        "nom": "Manoir hanté",
        "description": "Son de fantome dans un manoir",
        "duree": datetime.timedelta(seconds=30),
        "id_freesound": "445936",
        "id_son": "pmUjYtf7",
        "tags": ["manoir", "fantome", "scary"],
        "cooldown_min": 3,
        "cooldown_max": 15,
    }


Son_m = Son_Manuel(
    nom="Bruits de pas",
    description="Bruits de pas qui s'approchent",
    duree=datetime.timedelta(seconds=59),
    id_freesound="662970",
    id_son="8cDmPouX",
    tags=["step", "approaching"],
    start_key="p",
)


sc = Scene(
    nom="Forêt Mystique",
    description="Une scène calme dans une forêt mystérieuse",
    id_scene="234567",
    sons_aleatoires=[son_a],
    sons_manuels=[Son_m],
    sons_continus=[Son_c, Son_c2],
    date_creation=datetime.date(2023, 10, 9),
)


pygame.init()
SceneService().jouer_scene(scene=sc)"""
# os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# ResetDatabase().ResetALL()

"""def arr():
    input("Appuyer sur Entrée pour arrêter le son")
    print("BB chat")

arr()

import os
import requests
from dotenv import load_dotenv
from typing import Dict, List, Optional, Union
from src.service.freesound import Freesound


dico_filtres = {"query": "violon", "min_duration": 80, "max_duration": None}
a = Freesound.rechercher_multi_filtres(dico_filtres=dico_filtres, limit=15)
print(a)

"""

import pygame, os, sys
import time

pygame.init()
pygame.mixer.init()  # Lancer le mixer pygame
son1 = Son_Manuel(
    nom="Musique douce",
    description="Musique douce au piano",
    duree=datetime.timedelta(minutes=20),
    id_freesound="182395",
    id_son="e6uKHU85",
    tags=["piano", "calm", "soft"],
    start_key="1",
)
son2 = Son_Continu(
    nom="Musique douce",
    description="Musique douce au piano",
    duree=datetime.timedelta(minutes=20),
    id_freesound="747222",
    id_son="e6uKHU85",
    tags=["piano", "calm", "soft"],
)
son3 = Son_Continu(
    nom="Musique douce",
    description="Musique douce au piano",
    duree=datetime.timedelta(minutes=20),
    id_freesound="662970",
    id_son="e6uKHU85",
    tags=["piano", "calm", "soft"],
)
scene1 = Scene(
    nom="Scene1",
    description="Description de la Scene1",
    id_scene="ZCokXpxM",
    sons_aleatoires=[],
    sons_continus=[son2, son3],
    sons_manuels=[son1],
    date_creation=datetime.date.today(),
)
# SceneService().jouer_scene(scene=scene1)

Freesound().supprimer_son(id_freesound="593074")

"""scene1 = Scene(
    nom="Scene1",
    description="Description de la Scene1",
    id_scene="ZCokXpxM",
    sons_aleatoires=[],
    sons_continus=[],
    sons_manuels=[],
    date_creation=datetime.date.today(),
)
Session().scene_to_param = scene1
son = SonService().instancier_son_par_id_type(
    id_freesound="249135", type_son="ALEATOIRE", schema="ProjetInfo"
)
print(son)
print(son.id_freesound)
print(type(son))
print(son.tags)
print(son.duree)"""
"""TagDAO().ajouter_tag(tag="first", schema="ProjetInfo")
TagDAO().ajouter_tag(tag="second", schema="ProjetInfo")
TagDAO().ajouter_tag(tag="third", schema="ProjetInfo")
TagDAO().ajouter_association_son_tag(id_freesound="249135", tag="first", schema="ProjetInfo")
TagDAO().ajouter_association_son_tag(id_freesound="249135", tag="second", schema="ProjetInfo")
TagDAO().ajouter_association_son_tag(id_freesound="249135", tag="third", schema="ProjetInfo")"""
"""
LICENSEson = Son_Continu(
    nom="The Imperial March",
    description="Luke, I am your father",
    duree=datetime.timedelta(seconds=45),
    id_freesound="747222__gregorquendel__tchaikovsky-dance-of-the-sugar-plum-fairy-the-nutcracker-suite-op",
    tags=["starwars", "Vador", "JW"],
)

LICENSEson.jouer_son()
"""
"""
res = Freesound.rechercher_par_tag(tag="piano", limit=15)
print(res)
"""
"""
son_alea1 = Son_Aleatoire(
    "SonAlea1", "Description du SonAlea1", datetime.timedelta(seconds=1), "194863", [], 10, 15
)
son_alea2 = Son_Aleatoire(
    "SonAlea2", "Description du SonAlea2", datetime.timedelta(seconds=2), "249135", [], 20, 25
)
son_continu1 = Son_Continu(
    "SonContinu1", "Description du SonContinu1", datetime.timedelta(seconds=5), "123456", []
)
son_continu2 = Son_Continu(
    "SonContinu2", "Description du SonContinu2", datetime.timedelta(seconds=10), "234567", []
)
son_manuel1 = Son_Manuel(
    "SonManuel1", "Description du SonManuel1", datetime.timedelta(seconds=4), "134679", [], "a"
)
son_manuel2 = Son_Manuel(
    "SonManuel2", "Description du SonManuel2", datetime.timedelta(seconds=8), "258258", [], "b"
)
son_dao = SonDAO()
son_dao.ajouter_son(son_alea1, "ProjetInfo")
son_dao.ajouter_son(son_alea2, "ProjetInfo")
son_dao.ajouter_son(son_continu1, "ProjetInfo")
son_dao.ajouter_son(son_continu2, "ProjetInfo")
son_dao.ajouter_son(son_manuel1, "ProjetInfo")
son_dao.ajouter_son(son_manuel2, "ProjetInfo")
son_dao.ajouter_association_scene_son(id_scene="ZCokXpxM", son=son_alea1, schema="ProjetInfo")
son_dao.ajouter_association_scene_son(id_scene="ZCokXpxM", son=son_alea2, schema="ProjetInfo")
son_dao.ajouter_association_scene_son(id_scene="ZCokXpxM", son=son_continu1, schema="ProjetInfo")
son_dao.ajouter_association_scene_son(id_scene="ZCokXpxM", son=son_continu2, schema="ProjetInfo")
son_dao.ajouter_association_scene_son(id_scene="ZCokXpxM", son=son_manuel1, schema="ProjetInfo")
son_dao.ajouter_association_scene_son(id_scene="ZCokXpxM", son=son_manuel2, schema="ProjetInfo")


sounddeck1 = SD(
    nom="SoundDeck 1",
    description="First sound deck",
    id_sd="101",
    scenes=[],
    date_creation=datetime.date.today(),
    id_createur="123",
)
print(sounddeck1)
print(sounddeck1.id_sd)
scene1 = Scene(
    nom="Scene1",
    description="Description de la Scene1",
    id_scene="pIbHf1",
    sons_aleatoires=[],
    sons_continus=[],
    sons_manuels=[],
    date_creation=datetime.date.today(),
)

scene2 = Scene(
    nom="Scene2",
    description="Description de la Scene2",
    id_scene="2PjUy",
    sons_aleatoires=[],
    sons_continus=[],
    sons_manuels=[],
    date_creation=datetime.date.today(),
)

SceneDAO().ajouter_scene(scene1, schema="SchemaTest")
print("ajout 1 ok")
SceneDAO().ajouter_scene(scene2, schema="SchemaTest")
print("ajout 2 ok")


# User class instantiation
user1 = User(
    nom="Nom1",
    prenom="Prenom1",
    date_naissance=datetime.date(2001, 1, 1),
    id_user="123",
    SD_possedes=[],
    mdp="Password1!",
    pseudo="nom.prenom1",
)
user2 = User(
    nom="Nom2",
    prenom="Prenom2",
    date_naissance=datetime.date(2002, 2, 2),
    id_user="222222",
    SD_possedes=[],
    mdp="Password2!",
    pseudo="nom.prenom2",
)

# SD (SoundDeck) class instantiation with empty scenes list
sounddeck1 = SD(
    nom="SoundDeck 1",
    description="First sound deck",
    id_sd="101",
    scenes=[],
    date_creation=datetime.date.today(),
    id_createur="123",
)
sounddeck2 = SD(
    nom="SoundDeck 2",
    description="Second sound deck",
    id_sd="102",
    scenes=[],
    date_creation=datetime.date.today(),
    id_createur="222222",
)
sounddeck3 = SD(
    nom="SoundDeck 3",
    description="Third sound deck",
    id_sd="103",
    scenes=[],
    date_creation=datetime.date.today(),
    id_createur="123",
)
sounddeck4 = SD(
    nom="SoundDeck 4",
    description="Fourth sound deck",
    id_sd="104",
    scenes=[],
    date_creation=datetime.date.today(),
    id_createur="222222",
)

# Scene class instantiation

scene1 = Scene(
    nom="Scene1",
    description="Description de la Scene1",
    id_scene="123123",
    sons_aleatoires=[],
    sons_continus=[],
    sons_manuels=[],
    date_creation=datetime.date.today(),
)
scene2 = Scene(
    nom="Scene2",
    description="Description de la Scene2",
    id_scene="234234",
    sons_aleatoires=[],
    sons_continus=[],
    sons_manuels=[],
    date_creation=datetime.date.today(),
)
scene3 = Scene(
    nom="Scene3",
    description="Description de la Scene3",
    id_scene="345345",
    sons_aleatoires=[],
    sons_continus=[],
    sons_manuels=[],
    date_creation=datetime.date.today(),
)
scene4 = Scene(
    nom="Scene4",
    description="Description de la Scene4",
    id_scene="456456",
    sons_aleatoires=[],
    sons_continus=[],
    sons_manuels=[],
    date_creation=datetime.date.today(),
)
# Scene class instantiation

son_alea1 = Son_Aleatoire(
    "SonAlea1", "Description du SonAlea1", datetime.timedelta(seconds=1), "194863", [], 10, 15
)
son_alea2 = Son_Aleatoire(
    "SonAlea2", "Description du SonAlea2", datetime.timedelta(seconds=2), "249135", [], 20, 25
)
son_continu1 = Son_Continu(
    "SonContinu1", "Description du SonContinu1", datetime.timedelta(seconds=5), "123456", []
)
son_continu2 = Son_Continu(
    "SonContinu2", "Description du SonContinu2", datetime.timedelta(seconds=10), "234567", []
)
son_manuel1 = Son_Manuel(
    "SonManuel1", "Description du SonManuel1", datetime.timedelta(seconds=4), "134679", [], "a"
)
son_manuel2 = Son_Manuel(
    "SonManuel2", "Description du SonManuel2", datetime.timedelta(seconds=8), "258258", [], "b"
)


son_dao = SonDAO()
sd_dao = SDDAO()
user_dao = UserDAO()
scene_dao = SceneDAO()
user_dao.ajouter_user(user1, "SchemaTest")
user_dao.ajouter_user(user2, "SchemaTest")
sd_dao.ajouter_sd(sounddeck1, "SchemaTest")
sd_dao.ajouter_sd(sounddeck2, "SchemaTest")
sd_dao.ajouter_sd(sounddeck3, "SchemaTest")
sd_dao.ajouter_sd(sounddeck4, "SchemaTest")
scene_dao.ajouter_scene(scene1, "Schematest")
scene_dao.ajouter_scene(scene2, "Schematest")
scene_dao.ajouter_scene(scene3, "Schematest")
scene_dao.ajouter_scene(scene4, "Schematest")
son_dao.ajouter_son(son_alea1, "SchemaTest")
son_dao.ajouter_son(son_alea2, "SchemaTest")
son_dao.ajouter_son(son_continu1, "SchemaTest")
son_dao.ajouter_son(son_continu2, "SchemaTest")
son_dao.ajouter_son(son_manuel1, "SchemaTest")
son_dao.ajouter_son(son_manuel2, "SchemaTest")

all_users = user_dao.consulter_users(schema="SchemaTest")
all_sds = sd_dao.consulter_sds(schema="SchemaTest")
all_scenes = scene_dao.consulter_scenes(schema="SchemaTest")
all_sons = son_dao.consulter_sons(schema="Schematest")
# print(all_users)
# print(all_sds)
# print(all_scenes)
# print(all_sons)
scene_dao.ajouter_association_sd_scene(id_sd="101", id_scene="123123", schema="SchemaTest")
scene_dao.ajouter_association_sd_scene(id_sd="101", id_scene="234234", schema="SchemaTest")
scene_dao.ajouter_association_sd_scene(id_sd="101", id_scene="345345", schema="SchemaTest")
scene_dao.ajouter_association_sd_scene(id_sd="102", id_scene="234234", schema="SchemaTest")
scene_dao.ajouter_association_sd_scene(id_sd="103", id_scene="345345", schema="SchemaTest")
scene_dao.ajouter_association_sd_scene(id_sd="104", id_scene="456456", schema="SchemaTest")
son_dao.ajouter_association_scene_son(id_scene="123123", son=son_alea1, schema="SchemaTest")
son_dao.ajouter_association_scene_son(id_scene="123123", son=son_continu1, schema="SchemaTest")
son_dao.ajouter_association_scene_son(id_scene="123123", son=son_manuel1, schema="SchemaTest")
son_dao.ajouter_association_scene_son(id_scene="234234", son=son_alea2, schema="SchemaTest")
son_dao.ajouter_association_scene_son(id_scene="234234", son=son_continu2, schema="SchemaTest")
son_dao.ajouter_association_scene_son(id_scene="234234", son=son_manuel2, schema="SchemaTest")
son_dao.ajouter_association_scene_son(id_scene="234234", son=son_continu1, schema="SchemaTest")
sd_dao.ajouter_association_user_sd(id_user="123", id_sd="101", schema="SchemaTest")
sd_dao.ajouter_association_user_sd(id_user="222222", id_sd="101", schema="SchemaTest")
print(all_users)
print(all_sds)
print(all_scenes)
print(all_sons)
sd_dao.supprimer_toutes_associations_sd(id_sd="101", schema="SchemaTest")
"""
"""print(
    son_dao.check_if_son_in_scene(
        id_scene="123123", id_freesound="194863", type_son="aleatoire", schema="SchemaTest"
    )
)  # T
print(
    son_dao.check_if_son_in_scene(
        id_scene="123123", id_freesound="123456", type_son="continu", schema="SchemaTest"
    )
)  # T
print(
    son_dao.check_if_son_in_scene(
        id_scene="123123", id_freesound="134679", type_son="manuel", schema="SchemaTest"
    )
)  # T
print(
    son_dao.check_if_son_in_scene(
        id_scene="234234", id_freesound="123456", type_son="continu", schema="SchemaTest"
    )
)  # T
print(
    son_dao.check_if_son_in_scene(
        id_scene="234234", id_freesound="134679", type_son="manuel", schema="SchemaTest"
    )
)  # F

print(son_dao.rechercher_sons_par_scene(id_scene="123123", schema="SchemaTest"))
print(son_dao.rechercher_sons_par_scene(id_scene="234234", schema="SchemaTest"))
print(
    son_dao.supprimer_association_scene_son(
        id_scene="123123", id_freesound="194863", type_son="aleatoire", schema="SchemaTest"
    )
)
print(son_dao.rechercher_sons_par_scene(id_scene="123123", schema="SchemaTest"))
ResetDatabase().ResetALL()"""
