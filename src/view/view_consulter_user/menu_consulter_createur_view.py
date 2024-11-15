from view.abstractview import AbstractView
from colorama import Fore, Style
from InquirerPy import prompt

####
from service.user_service import UserService

####
from view.abstractview import AbstractView

# from view.view_consulter_user.menu_consulter_createur_view import ConsulterCreateurView
# from view.view_consulter_user.menu_consulter_nom_view import ConsulterNomView


class ConsulterCreateurView:
    "test"

    def __init__(self):
        super().__init__()
        self.question_createur = [
            {
                "type": "input",
                "name": "createur",
                "message": "Entrez le pseudo du créateur souhaité :",
            },
        ]

    def display_info(self):
        print(Fore.BLUE + " MENU DE CONSULTATION [CREATEUR] ".center(80, "=") + Style.RESET_ALL)
