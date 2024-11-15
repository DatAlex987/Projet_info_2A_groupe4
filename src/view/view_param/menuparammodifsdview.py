"""Ce module implémente la view dédiée la modification du SD d'un utilisateur"""

from colorama import Fore, Style
from InquirerPy import prompt
from view.abstractview import AbstractView
from view.session import Session
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_continu import Son_Continu
from business_object.son_manuel import Son_Manuel
from service.sd_service import SDService
from service.scene_service import SceneService
from service.son_service import SonService


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
            pass  # méthode service pour display les infos de la SD
        elif choix_modif["choix modif"] == "Modifier le nom":
            new_nom = prompt(self.question_modif_nom)
            SDService().modifier_nom_sd(
                sd=Session().sd_to_param, new_nom=new_nom["modif nom"], schema="ProjetInfo"
            )
        elif choix_modif["choix modif"] == "Modifier la description":
            new_desc = prompt(self.question_modif_desc)
            SDService().modifier_desc_sd(
                sd=Session().sd_to_param, new_desc=new_desc["modif desc"], schema="ProjetInfo"
            )

        print(
            Fore.GREEN + "Modification effectuée avec succès" + Style.RESET_ALL
        )  # A déplacer pour ne pas l'afficher automatiquement
        from view.view_param.menuparamsdview import MenuParamSDView

        return MenuParamSDView()

    def display_info(self):
        print(Fore.BLUE + " MENU DE PARAMETRAGE ".center(80, "=") + Style.RESET_ALL)
