from view.abstractview import AbstractView
from colorama import Fore, Style
from InquirerPy import prompt
from view.abstractview import AbstractView
from view.menuprincipalview import MenuPrincipalView
from service.user_service import UserService


class MenuSDView(AbstractView):
    "classe représentant l'accès au menu sound-deck, après le menu principal"
