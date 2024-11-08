from view.abstractview import AbstractView
from colorama import Fore, Style
from InquirerPy import prompt
from view.abstractview import AbstractView
from view.menuprincipalview import MenuPrincipalView
from service.user_service import UserService


class MenuSceneView(AbstractView):
    "classe représentant l'accès au menu scène, après le menu principal"
