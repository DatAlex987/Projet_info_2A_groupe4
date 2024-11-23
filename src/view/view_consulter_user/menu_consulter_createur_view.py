from colorama import Fore, Style
from InquirerPy import prompt

####
from service.user_service import UserService

####
from view.abstractview import AbstractView
from view.view_consulter_user.consulter_users_proches_view import ConsulterUsersProchesView


class ConsulterCreateurView(AbstractView):

    def __init__(self):
        super().__init__()
        self.question_createur = [
            {
                "type": "input",
                "name": "createur",
                "message": "Entrez le pseudo du créateur souhaité :",
            },
        ]

    def make_choice(self):
        createur_voulu = prompt(self.question_createur)
        UserService().FindCloseNameUsers(
            pseudo_approx=createur_voulu["createur"], schema="ProjetInfo"
        )
        # Rechercher tous les users qui ont un pseudo proche
        # La liste des Users ayant un nom proche sera stocké en Session
        # Puis, envoyer vers une view pour sélectionner le créateur que l'on veut consulter.
        return ConsulterUsersProchesView()

    def display_info(self):
        print(Fore.BLUE + " [JEU] MENU RECHERCHE CREATEUR ".center(80, "=") + Style.RESET_ALL)
