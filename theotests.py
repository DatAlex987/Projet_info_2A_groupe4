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
from business_object.son import Son
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_manuel import Son_Manuel
from business_object.son_continu import Son_Continu
import hashlib
import pygame

ResetDatabase().ResetALL()

pygame.mixer.init


"""
prenom = "bob"
nom = "Hessane"

mdp = "12345663"
mdp_combine = mdp + prenom

mdph = hashlib.pbkdf2_hmac("sha256", mdp_combine.encode("utf-8"), nom.encode("utf-8"), 100000)
print(mdp_combine, mdph)
print(hashlib.pbkdf2_hmac("sha256", mdp_combine.encode("utf-8"), nom.encode("utf-8"), 100000))

def f(son):
    if isinstance(son, Son_Aleatoire):
        return "alea"
    if isinstance(son, Son_Continu):
        return "continu"


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
)
sounddeck2 = SD(
    nom="SoundDeck 2",
    description="Second sound deck",
    id_sd="102",
    scenes=[],
    date_creation=datetime.date.today(),
)
sounddeck3 = SD(
    nom="SoundDeck 3",
    description="Third sound deck",
    id_sd="103",
    scenes=[],
    date_creation=datetime.date.today(),
)
sounddeck4 = SD(
    nom="SoundDeck 4",
    description="Fourth sound deck",
    id_sd="104",
    scenes=[],
    date_creation=datetime.date.today(),
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
print(all_sons)
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


print(
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
ResetDatabase().ResetALL()
"""
