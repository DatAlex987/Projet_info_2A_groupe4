"""Ce module implémente la view dédiée au paramétrage des Scènes/Sound-deck de l'utilisateur"""

from colorama import Fore, Style
from InquirerPy import prompt
from service.sd_service import SDService
from dao.sd_dao import SDDAO
####
from view.session import Session
from view.abstractview import AbstractView
from view.menuprincipalview import MenuPrincipalView
from view.view_param.menuparamsdview import MenuParamSDView

class MenuParamView(AbstractView):
    """Classe représentant la view de paramétrage des Scènes/Sound-deck"""

    def __init__(self):
        super().__init__()
        self.question = [
            {
                "type": "list",
                "name": "Premier Choix",
                "message": "Que souhaitez-vous faire ?",
                "choices": [
                    "Consulter/Modifier une de mes sound-decks",
                    "Créer une sound-deck",
                    "Retour au menu principal",
                ],
            }
        ]
        self.questions_creation_sd = [
            {
                "type": "input",
                "name": "nom",
                "message": "Quel sera le nom de votre sound-deck ?",
            },
            {
                "type": "input",
                "name": "description",
                "message": "Quelle sera la description de votre sound-deck ?",
            },
        ]

    def make_choice(self):
        choix = prompt(self.question)
        if choix["Premier Choix"] == "Consulter/Modifier une de mes sound-decks":
            next_view = MenuParamSDView()
        elif choix["Premier Choix"] == "Créer une sound-deck":
            sd_creee_avec_succes = False
            while not sd_creee_avec_succes:
                try:
                    infos_creation_sd = prompt(self.questions_creation_sd)
                    if SDService().creer_sd(
                        nom=infos_creation_sd["nom"],
                        description=infos_creation_sd["description"],
                        schema="ProjetInfo",
                    ):
                        print(
                            Fore.GREEN
                            + f"Sound-deck '{infos_creation_sd['nom']}' créée avec succès"
                            + Style.RESET_ALL
                        )
                        sd_creee_avec_succes = True
                except ValueError as e:
                    print(
                        Fore.RED
                        + f"Erreur lors de la création de la Sound-deck : {e}"
                        + Style.RESET_ALL
                    )
            next_view = MenuParamView()
        elif choix["Premier Choix"] == "Retour au menu principal":
            next_view = MenuPrincipalView()
        return next_view

    def display_info(self):
        print(Fore.BLUE + " MENU DE PARAMETRAGE ".center(80, "=") + Style.RESET_ALL)
