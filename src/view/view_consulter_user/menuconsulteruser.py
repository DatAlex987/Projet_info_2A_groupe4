from colorama import Fore, Style
from InquirerPy import prompt

####
from service.session import Session

####
from view.abstractview import AbstractView
from view.view_consulter_user.menu_consulter_createur_view import ConsulterCreateurView
from view.view_consulter_user.menu_consulter_nom_view import ConsulterNomView


class MenuConsulterUserView(AbstractView):
    """classe représentant l'accès au menu de consultations des créations des utilisateurs, après le
    menu principal"""

    def __init__(self):
        super().__init__()
        self.question = [
            {
                "type": "list",
                "name": "Premier Choix",
                "message": "Comment souhaitez-vous rechercher les SD ?",
                "choices": [
                    "Rechercher par nom",
                    "Rechercher par créateur",
                    "Retour au menu principal",
                ],
            }
        ]

    def make_choice(self):
        choix = prompt(self.question)
        if choix["Premier Choix"] == "Rechercher par nom":
            Session().type_recherche_consult = "nom"
            next_view = ConsulterNomView()
        elif choix["Premier Choix"] == "Rechercher par créateur":
            Session().type_recherche_consult = "user"
            next_view = ConsulterCreateurView()
        elif choix["Premier Choix"] == "Retour au menu principal":
            from view.menuprincipalview import MenuPrincipalView

            next_view = MenuPrincipalView()
        return next_view

    def display_info(self):
        print(Fore.BLUE + " [CONSULTATION] ".center(80, "=") + Style.RESET_ALL)
