"""Ce module implémente la view dédiée la modification du SD d'un utilisateur"""

from colorama import Fore, Style
from InquirerPy import prompt

####
from service.session import Session
from service.sd_service import SDService

####
from view.abstractview import AbstractView


class MenuParamModifSDView(AbstractView):
    """Classe représentant la view de la modification d'un sound-deck"""

    def __init__(self):
        super().__init__()

        self.question_modif_sd = [
            {
                "type": "list",
                "name": "choix modif",
                "message": "Que souhaitez-vous faire ?",
                "choices": [
                    "Voir la fiche de la sound-deck",
                    "Modifier le nom",
                    "Modifier la description",
                ],
            }
        ]

        self.question_modif_nom = [
            {
                "type": "input",
                "name": "modif nom",
                "message": "Entrez le nouveau nom pour cette sound-deck:",
            }
        ]
        self.question_modif_desc = [
            {
                "type": "input",
                "name": "modif desc",
                "message": "Entrez la nouvelle description pour cette sound-deck:",
            }
        ]

    def make_choice(self):
        choix_modif = prompt(self.question_modif_sd)
        if choix_modif["choix modif"] == "Voir la fiche de la sound-deck":
            SDService().afficher_details_sd(Session().sd_to_param)
        elif choix_modif["choix modif"] == "Modifier le nom":
            new_nom = prompt(self.question_modif_nom)
            SDService().modifier_nom_sd(
                sd=Session().sd_to_param, new_nom=new_nom["modif nom"], schema="ProjetInfo"
            )
            print(Fore.GREEN + "Modification effectuée avec succès" + Style.RESET_ALL)

        elif choix_modif["choix modif"] == "Modifier la description":
            new_desc = prompt(self.question_modif_desc)
            SDService().modifier_desc_sd(
                sd=Session().sd_to_param, new_desc=new_desc["modif desc"], schema="ProjetInfo"
            )
            print(Fore.GREEN + "Modification effectuée avec succès" + Style.RESET_ALL)

        from view.view_param.menuparamsdview import MenuParamSDView

        return MenuParamSDView()

    def display_info(self):
        print(Fore.BLUE + " [PARAMETRAGE] MENU SOUND-DECK ".center(80, "=") + Style.RESET_ALL)
