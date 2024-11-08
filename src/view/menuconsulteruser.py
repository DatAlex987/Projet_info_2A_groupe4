from view.abstractview import AbstractView
from colorama import Fore, Style
from InquirerPy import prompt
from view.abstractview import AbstractView
from view.menuprincipalview import MenuPrincipalView
from service.user_service import UserService


class MenuConsulterUserView(AbstractView):
    "classe représentant l'accès au menu de consultations des créations des utilisateurs, après le menu principal"
