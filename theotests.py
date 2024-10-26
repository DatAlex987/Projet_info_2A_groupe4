from src.dao.db_connection import DBConnection
from src.business_object.user import User
from src.business_object.personne import Personne
from src.business_object.sd import SD
import datetime
from utils.reset_database import ResetDatabase
from src.dao.user_dao import UserDAO
from src.dao.sd_dao import SDDAO

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

sd_dao = SDDAO()
user_dao = UserDAO()
user_dao.ajouter_user(user1, "SchemaTest")
user_dao.ajouter_user(user2, "SchemaTest")
sd_dao.ajouter_sd(sounddeck1, "SchemaTest")
sd_dao.ajouter_sd(sounddeck2, "SchemaTest")
sd_dao.ajouter_sd(sounddeck3, "SchemaTest")
sd_dao.ajouter_sd(sounddeck4, "SchemaTest")
all_users = user_dao.consulter_users(schema="SchemaTest")
all_sds = sd_dao.consulter_sds(schema="SchemaTest")
# print(all_users)
# print(all_sds)
sd_dao.ajouter_association_user_sd(id_user="123", id_sd="101", schema="SchemaTest")
sd_dao.ajouter_association_user_sd(id_user="123", id_sd="102", schema="SchemaTest")
sd_dao.ajouter_association_user_sd(id_user="222222", id_sd="103", schema="SchemaTest")
sd_dao.ajouter_association_user_sd(id_user="222222", id_sd="104", schema="SchemaTest")
print(sd_dao.supprimer_association_user_sd(id_user="123", id_sd="102", schema="SchemaTest"))
print(sd_dao.rechercher_sds_par_user(id_user="123", schema="SchemaTest"))
print(sd_dao.check_if_sd_in_user(id_user="123", id_sd="102", schema="SchemaTest"))
