from view.abstractview import AbstractView
from colorama import Fore, Style
from InquirerPy import prompt

####
# from service.user_service import UserService

####
from view.menuconsulteruser import MenuConsulterUserView
from view.menu_jeu_view import MenuJeuView

# from view.abstractview import AbstractView


class MenuPrincipalView(AbstractView):
    "classe représentant l'accès au menu principal, une fois l'utilisateur connecté avec succès."

    def __init__(self):
        super().__init__()
        self.question = [
            {
                "type": "list",
                "name": "Menu principal",
                "message": "Que souhaitez-vous faire ?",
                "choices": [
                    "Accéder au menu de paramétrage",
                    "Accéder au menu de jeu",
                    "Consulter les créations des utilisateurs",
                    "Se déconnecter",
                ],
            }
        ]

    def make_choice(self):
        answers = prompt(self.question)
        if answers["Menu principal"] == "Accéder au menu de paramétrage":
            from view.menuparam_view import MenuParamView

            next_view = MenuParamView()
        if answers["Menu principal"] == "Accéder au menu de jeu":
            next_view = MenuJeuView()
        if answers["Menu principal"] == "Consulter les créations des utilisateurs":
            next_view = MenuConsulterUserView()
        if answers["Menu principal"] == "Se déconnecter":
            # Contraint de faire l'import ici pour éviter les circular imports
            from view.accueilview import AccueilView

            next_view = AccueilView()

        return next_view

    def display_info(self):
        print(Fore.BLUE + " MENU PRINCIPAL ".center(80, "=") + Style.RESET_ALL)
