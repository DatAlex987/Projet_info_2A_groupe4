# from dao.db_connection import DBConnection
from dao.user_dao import UserDAO
from dao.son_dao import SonDAO
from business_object.son import Son
from utils.reset_database import ResetDatabase
from business_object.user import User
import datetime

ResetDatabase().lancer()
user_dao = UserDAO()
U = User(
    mdp="Mdpasse!123",
    date_naissance=datetime.date(1990, 2, 2),
    nom="TheOne",
    prenom="Neo",
    SD_possedes=[],
    id_user="123456",
)
print(user_dao.ajouter_user(U))
son_dao = SonDAO()
Sound = Son(
    nom="moteur",
    description="bruit d'un moteur V8",
    duree=datetime.time(0, 3, 52),
    id_freesound="481395",
    tags=["voiture", "moteur", "puissance"],
)
print(son_dao.ajouter_son(Sound))
