# from dao.db_connection import DBConnection
from dao.user_dao import UserDAO
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
print(user_dao.ajouter_user(U, schema="ProjetInfo"))
