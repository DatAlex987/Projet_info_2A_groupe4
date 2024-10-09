from dao.db_connection import DBConnection
from dao.user_dao import UserDAO

print(UserDAO.ajouter_user("folsory", "mdp123", 99, "mail@mail.com"))
