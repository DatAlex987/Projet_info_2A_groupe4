# from dao.db_connection import DBConnection
from dao.user_dao import UserDAO
from dao.son_dao import SonDAO
from business_object.son import Son
from utils.reset_database import ResetDatabase
from business_object.user import User
import datetime

ResetDatabase().lancer()
print(
    UserDAO.ajouter_user(
        User(
            pseudo="PseudoEXEMPLE",
            mdp_hashe="Mdpasse!123",
            age=99,
            nom="TheOne",
            prenom="Neo",
        )
    )
)
son_dao = SonDAO()
Sound = Son(
    "moteur",
    "bruit d'un moteur V8",
    datetime.time(0, 3, 52),
    "481395",
    ["voiture", "moteur", "puissance"],
)
print(son_dao.ajouter_son(Sound))
