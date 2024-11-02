# from dao.db_connection import DBConnection
from dao.user_dao import UserDAO
from utils.reset_database import ResetDatabase
from business_object.user import User
from view.accueil_view import AccueilView
import datetime

reseter = ResetDatabase()
reseter.ResetALL()

User_info = ""  # Initialisation de User qui contiendra les infos de la personne
# en train d'utiliser l'application


view = AccueilView()

with open("resources/banner.txt", mode="r", encoding="utf-8") as title:
    print(title.read())

while view:
    view.display_info()
    view, User_info = view.make_choice(User_info)

with open("resources/exit.txt", mode="r", encoding="utf-8") as exit_message:
    print(exit_message.read())
