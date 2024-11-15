from view.abstractview import AbstractView
from colorama import Fore, Style
from InquirerPy import prompt

####
from service.user_service import UserService

####
from view.abstractview import AbstractView

# from view.view_consulter_user.menu_consulter_createur_view import ConsulterCreateurView
# from view.view_consulter_user.menu_consulter_nom_view import ConsulterNomView


class ConsulterSDsView(AbstractView):

    def __init__(self):
        super().__init__()
        self.question = [
            {
                "type": "list",
                "name": "Choix User",
                "message": (
                    "De quel utilisateur souhaitez-vous consulter les sound-decks ? \n"
                    " ID   |    Prénom    |     Nom       |    Pseudo             \n"
                    "----------------------------------------------------------------"
                ),
                "choices": UserService().formatage_question_users_to_consult(),
            }
        ]

    def make_choice(self):
        pass

    def display_info(self):
        print(Fore.BLUE + " MENU DE CONSULTATION [CREATEUR] ".center(80, "=") + Style.RESET_ALL)
