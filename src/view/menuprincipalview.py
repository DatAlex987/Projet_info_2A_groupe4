from view.abstractview import AbstractView
from colorama import Fore, Style
from InquirerPy import prompt
from view.abstractview import AbstractView
from view.menuprincipalview import MenuPrincipalView
from service.user_service import UserService
from view.menusceneview import MenuSceneView
from view.menusdview import MenuSDView
from view.menuconsulteruser import MenuConsulterUserView

# est-ce que le diagramme d'activité est toujours d'actualité ??
# deconnexion : se deconnecter + retour ecran accueil


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
                    "Accéder au menu sound-deck",
                    "Accéder au menu scène",
                    "Consulter les créations des utilisateurs",
                ],
            }
        ]

    def make_choice(self):
        answers = prompt(self.question)
        if answers["Menu principal"] == "Accéder au menu sound-deck":
            next_view = MenuSDView()
        if answers["Menu principal"] == "Accéder au menu scène":
            next_view = MenuSceneView()
        if answers["Menu principal"] == "Consulter les créations des utilisateurs":
            next_view = MenuConsulterUserView()

        return next_view

    def display_info(self):
        print(Fore.BLUE + " MENU PRINCIPAL' ".center(80, "=") + Style.RESET_ALL)
