from dao.db_connection import DBConnection
from dao.user_dao import UserDAO
from utils.reset_database import ResetDatabase

ResetDatabase().lancer()
print(UserDAO.ajouter_user("folsory", "mdp123", 99, "mail@mail.com"))
