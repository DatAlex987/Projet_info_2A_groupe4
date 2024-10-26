from src.dao.db_connection import DBConnection
from src.business_object.user import User
from src.business_object.personne import Personne
from src.business_object.scene import Scene
from src.business_object.sd import SD
import datetime
from utils.reset_database import ResetDatabase
from src.dao.user_dao import UserDAO
from src.dao.sd_dao import SDDAO
from src.dao.scene_dao import SceneDAO

ResetDatabase().ResetALL()

# User class instantiation
user1 = User(
    nom="Nom1",
    prenom="Prenom1",
    date_naissance=datetime.date(2001, 1, 1),
    id_user="123",
    SD_possedes=[],
    mdp="Password1!",
)
user2 = User(
    nom="Nom2",
    prenom="Prenom2",
    date_naissance=datetime.date(2002, 2, 2),
    id_user="222222",
    SD_possedes=[],
    mdp="Password2!",
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
"""sd_dao = SDDAO()
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
all_users = user_dao.consulter_users(schema="SchemaTest")
all_sds = sd_dao.consulter_sds(schema="SchemaTest")
all_scenes = scene_dao.consulter_scenes(schema="SchemaTest")
# print(all_users)
# print(all_sds)
print(all_scenes)
scene_dao.ajouter_association_sd_scene(id_sd="101", id_scene="123123", schema="SchemaTest")
scene_dao.ajouter_association_sd_scene(id_sd="101", id_scene="234234", schema="SchemaTest")
scene_dao.ajouter_association_sd_scene(id_sd="101", id_scene="345345", schema="SchemaTest")
scene_dao.ajouter_association_sd_scene(id_sd="102", id_scene="234234", schema="SchemaTest")
scene_dao.ajouter_association_sd_scene(id_sd="103", id_scene="345345", schema="SchemaTest")
scene_dao.ajouter_association_sd_scene(id_sd="104", id_scene="456456", schema="SchemaTest")

print(scene_dao.check_if_scene_in_sd(id_sd="101", id_scene="234234", schema="SchemaTest"))
print(scene_dao.rechercher_scenes_par_sd(id_sd="101", schema="SchemaTest"))
print(scene_dao.supprimer_association_sd_scene(id_sd="101", id_scene="234234", schema="SchemaTest"))
print(scene_dao.check_if_scene_in_sd(id_sd="101", id_scene="234234", schema="SchemaTest"))
print(scene_dao.rechercher_scenes_par_sd(id_sd="101", schema="SchemaTest"))"""

ResetDatabase().ResetALL()
