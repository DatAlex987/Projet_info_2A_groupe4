from view.abstractview import AbstractView
from colorama import Fore, Style
from InquirerPy import prompt

####
from view.abstractview import AbstractView

####
from service.user_service import UserService
from service.sd_service import SDService
from service.scene_service import SceneService


class MenuJeuSonsView(AbstractView):
    "classe représentant l'accès au menu jeu, après le menu principal"
