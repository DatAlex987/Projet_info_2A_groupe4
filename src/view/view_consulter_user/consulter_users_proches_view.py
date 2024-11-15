from view.abstractview import AbstractView
from colorama import Fore, Style
from InquirerPy import prompt

####
from service.user_service import UserService

####
from view.abstractview import AbstractView

# from view.view_consulter_user.menu_consulter_createur_view import ConsulterCreateurView
# from view.view_consulter_user.menu_consulter_nom_view import ConsulterNomView


class ConsulterUsersProchesView(AbstractView):

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
        createur_voulu = prompt(self.question)
        id_select = createur_voulu["Choix User"].split()[1].strip("|")
        print(id_select)
        # Session().user_to_consult = UserService().instancier_par_id_user(id_user)
        return ConsulterUsersProchesView()

    def display_info(self):
        print(Fore.BLUE + " MENU DE CONSULTATION [CREATEUR] ".center(80, "=") + Style.RESET_ALL)
