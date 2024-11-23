"""Ce module implémente la view dédiée la modification d'un son de l'utilisateur"""

from colorama import Fore, Style
from InquirerPy import prompt

####
from service.session import Session
from service.son_service import SonService
from service.scene_service import SceneService
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_continu import Son_Continu
from business_object.son_manuel import Son_Manuel

####
from view.abstractview import AbstractView
from view.view_param.menuparamsceneview import MenuParamSceneView


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
                    "Modifier la description",
                    "Modifier le cooldown minimal",
                    "Modifier le cooldown maximal",
                    "Supprimer le son",
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
                    "Modifier la description",
                    "Modifier la touche de déclenchement",
                    "Supprimer le son",
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
                    "Modifier la description",
                    "Supprimer le son",
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
                "message": "Entrez la lettre de la touche avec laquelle vous souhaitez déclencher ce son (une lettre):",
            }
        ]
        self.question_modif_cdmin = [
            {
                "type": "input",
                "name": "modif cdmin",
                "message": "Entrez le nouveau cooldown minimal pour ce son:",
                "validate": lambda val: int(val) < Session().son_to_param.cooldown_max,
            }
        ]
        self.question_modif_cdmax = [
            {
                "type": "input",
                "name": "modif cdmax",
                "message": "Entrez le nouveau cooldown maximal pour ce son:",
                "validate": lambda val: int(val) > Session().son_to_param.cooldown_min,
            }
        ]

    def make_choice(self):
        if isinstance(Session().son_to_param, Son_Aleatoire):
            choix_modif = prompt(self.question_modif_alea)
            if choix_modif["choix modif"] == "Voir la fiche du son":
                SonService().afficher_details_son_aleatoire(Session().son_to_param)
            elif choix_modif["choix modif"] == "Modifier le nom":
                new_nom = prompt(self.question_modif_nom)
                SonService().modifier_nom_son(
                    son=Session().son_to_param, new_nom=new_nom["modif nom"], schema="ProjetInfo"
                )
            elif choix_modif["choix modif"] == "Modifier la description":
                new_desc = prompt(self.question_modif_desc)
                SonService().modifier_desc_son(
                    son=Session().son_to_param, new_desc=new_desc["modif desc"], schema="ProjetInfo"
                )
            elif choix_modif["choix modif"] == "Modifier le cooldown minimal":
                new_cdmin = prompt(self.question_modif_cdmin)
                SonService().modifier_cdmin_son(
                    son_alea=Session().son_to_param,
                    new_cdmin=new_cdmin["modif cdmin"],
                    schema="ProjetInfo",
                )
            elif choix_modif["choix modif"] == "Modifier le cooldown maximal":
                new_cdmax = prompt(self.question_modif_cdmax)
                SonService().modifier_cdmax_son(
                    son_alea=Session().son_to_param,
                    new_cdmax=new_cdmax["modif cdmax"],
                    schema="ProjetInfo",
                )
            elif choix_modif["choix modif"] == "Supprimer le son":
                SceneService().supprimer_son_existant(
                    son_to_delete=Session().son_to_param, schema="ProjetInfo"
                )
                print(Fore.GREEN + "Suppression du son effectuée avec succès" + Style.RESET_ALL)
                return MenuParamSceneView()

        elif isinstance(Session().son_to_param, Son_Continu):
            choix_modif = prompt(self.question_modif_continu)
            if choix_modif["choix modif"] == "Voir la fiche du son":
                SonService().afficher_details_son_continu(Session().son_to_param)
            elif choix_modif["choix modif"] == "Modifier le nom":
                new_nom = prompt(self.question_modif_nom)
                SonService().modifier_nom_son(
                    son=Session().son_to_param, new_nom=new_nom["modif nom"], schema="ProjetInfo"
                )
            elif choix_modif["choix modif"] == "Modifier la description":
                new_desc = prompt(self.question_modif_desc)
                SonService().modifier_desc_son(
                    son=Session().son_to_param, new_desc=new_desc["modif desc"], schema="ProjetInfo"
                )
            elif choix_modif["choix modif"] == "Supprimer le son":
                SceneService().supprimer_son_existant(
                    son_to_delete=Session().son_to_param, schema="ProjetInfo"
                )
                print(Fore.GREEN + "Suppression du son effectuée avec succès" + Style.RESET_ALL)
                return MenuParamSceneView()

        elif isinstance(Session().son_to_param, Son_Manuel):
            choix_modif = prompt(self.question_modif_manuel)
            if choix_modif["choix modif"] == "Voir la fiche du son":
                SonService().afficher_details_son_manuel(Session().son_to_param)
            elif choix_modif["choix modif"] == "Modifier le nom":
                new_nom = prompt(self.question_modif_nom)
                SonService().modifier_nom_son(
                    son=Session().son_to_param, new_nom=new_nom["modif nom"], schema="ProjetInfo"
                )
            elif choix_modif["choix modif"] == "Modifier la description":
                new_desc = prompt(self.question_modif_desc)
                SonService().modifier_desc_son(
                    son=Session().son_to_param, new_desc=new_desc["modif desc"], schema="ProjetInfo"
                )
                print(Fore.GREEN + "Modification effectuée avec succès" + Style.RESET_ALL)

            elif choix_modif["choix modif"] == "Modifier la touche de déclenchement":
                new_key = prompt(self.question_modif_key)
                SonService().modifier_start_key_son(
                    son_manuel=Session().son_to_param,
                    new_start_key=new_key["modif key"],
                    schema="ProjetInfo",
                )
                print(Fore.GREEN + "Modification effectuée avec succès" + Style.RESET_ALL)

            elif choix_modif["choix modif"] == "Supprimer le son":
                SceneService().supprimer_son_existant(
                    son_to_delete=Session().son_to_param, schema="ProjetInfo"
                )
                print(Fore.GREEN + "Suppression du son effectuée avec succès" + Style.RESET_ALL)
                return MenuParamSceneView()

        from view.view_param.menuparamscenespecifiqueview import MenuParamSceneSpecifiqueView

        return MenuParamSceneSpecifiqueView()

    def display_info(self):
        print(Fore.BLUE + " [PARAMETRAGE] MENU SON ".center(80, "=") + Style.RESET_ALL)
