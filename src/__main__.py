from utils.reset_database import ResetDatabase
from view.accueilview import AccueilView
from business_object.user import User
from dao.user_dao import UserDAO
import datetime

"""user1 = User(
    nom="San",
    prenom="Theo",
    date_naissance=datetime.date(2001, 5, 28),
    id_user="eft52",
    SD_possedes=[],
    mdp="MdpTheo3007!",
    pseudo="folsory",
)
UserDAO().ajouter_user(user1, "ProjetInfo")
"""
view = AccueilView()

with open("resources/banner.txt", mode="r", encoding="utf-8") as title:
    print(title.read())

while view:
    view.display_info()
    view = view.make_choice()

with open("resources/exit.txt", mode="r", encoding="utf-8") as exit_message:
    print(exit_message.read())
