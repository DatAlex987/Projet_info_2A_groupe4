"""Ce module implémente la view dédiée la modification d'un son de l'utilisateur"""

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


class MenuParamModifSonView(AbstractView):
    """Classe représentant la view de la modification d'un son"""

    def __init__(self):
        super().__init__()

        self.question_modif_alea = [
            {
                "type": "list",
                "name": "choix modif",
                "message": "Que souhaitez-vous faire ?",
                "choices": [
                    "Voir la fiche du son",
                    "Modifier le nom",
                    "Modifier sa description",
                    "Modifier le cooldown minimal",
                    "Modifier le cooldown maximal",
                ],
            }
        ]
        self.question_modif_manuel = [
            {
                "type": "list",
                "name": "choix modif",
                "message": "Que souhaitez-vous faire ?",
                "choices": [
                    "Voir la fiche du son",
                    "Modifier le nom",
                    "Modifier sa description",
                    "Modifier la touche de déclenchement",
                ],
            }
        ]
        self.question_modif_continu = [
            {
                "type": "list",
                "name": "choix modif",
                "message": "Que souhaitez-vous faire ?",
                "choices": [
                    "Voir la fiche du son",
                    "Modifier le nom",
                    "Modifier sa description",
                ],
            }
        ]
        self.question_modif_nom = [
            {
                "type": "input",
                "name": "modif nom",
                "message": "Entrez le nouveau nom pour ce son:",
            }
        ]
        self.question_modif_desc = [
            {
                "type": "input",
                "name": "modif desc",
                "message": "Entrez la nouvelle description pour ce son:",
            }
        ]
        self.question_modif_key = [
            {
                "type": "input",
                "name": "modif key",
                "message": "Entrez la lettre de la touche avec laquelle vous souhaitez déclencher ce son:",
            }
        ]
        self.question_modif_cdmin = [
            {
                "type": "input",
                "name": "modif cdmin",
                "message": "Entrez le nouveau cooldown minimal pour ce son:",
            }
        ]
        self.question_modif_cdmax = [
            {
                "type": "input",
                "name": "modif cdmax",
                "message": "Entrez le nouveau cooldown maximal pour ce son:",
            }
        ]

    def make_choice(self):  # NON TESTE YET
        dico_modifs = {"nom": None, "description": None, "param1": None, "param2": None}
        if isinstance(Session().son_to_param, Son_Aleatoire):
            choix_modif = prompt(self.question_modif_alea)
            if choix_modif["choix modif"] == "Voir la fiche du son":
                pass  # TO DO
            elif choix_modif["choix modif"] == "Modifier le nom":
                pass
            elif choix_modif["choix modif"] == "Modifier la description":
                pass
            elif choix_modif["choix modif"] == "Modifier le nom":
                pass
            elif choix_modif["choix modif"] == "Modifier le nom":
                pass
        elif isinstance(Session().son_to_param, Son_Continu):
            choix_modif = prompt(self.question_modif_continu)
        elif isinstance(Session().son_to_param, Son_Manuel):
            choix_modif = prompt(self.question_modif_manuel)
        return MenuParamSceneSpecifiqueView()

    def display_info(self):
        print(Fore.BLUE + " MENU DE PARAMETRAGE ".center(80, "=") + Style.RESET_ALL)
