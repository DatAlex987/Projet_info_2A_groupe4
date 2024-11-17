"""Ce module implémente la view dédiée la modification d'une scène d'un utilisateur"""

from colorama import Fore, Style
from InquirerPy import prompt
from view.abstractview import AbstractView
from service.session import Session
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_continu import Son_Continu
from business_object.son_manuel import Son_Manuel
from service.sd_service import SDService
from service.scene_service import SceneService
from service.son_service import SonService


class MenuParamModifSceneView(AbstractView):
    """Classe représentant la view de la modification d'une scène"""

    def __init__(self):
        super().__init__()

        self.question_modif_scene = [
            {
                "type": "list",
                "name": "choix modif",
                "message": "Que souhaitez-vous faire ?",
                "choices": [
                    "Voir la fiche de la scène",
                    "Modifier le nom",
                    "Modifier la description",
                ],
            }
        ]

        self.question_modif_nom = [
            {
                "type": "input",
                "name": "modif nom",
                "message": "Entrez le nouveau nom pour cette scène:",
            }
        ]
        self.question_modif_desc = [
            {
                "type": "input",
                "name": "modif desc",
                "message": "Entrez la nouvelle description pour cette scène (max. 280 caractères) :",
            }
        ]

    def make_choice(self):
        choix_modif = prompt(self.question_modif_scene)
        if choix_modif["choix modif"] == "Voir la fiche de la scène":
            pass  # méthode service pour display les infos de la scène
        elif choix_modif["choix modif"] == "Modifier le nom":
            new_nom = prompt(self.question_modif_nom)
            SceneService().modifier_nom_scene(
                scene=Session().scene_to_param, new_nom=new_nom["modif nom"], schema="ProjetInfo"
            )
            print(Fore.GREEN + "Modification effectuée avec succès" + Style.RESET_ALL)

        elif choix_modif["choix modif"] == "Modifier la description":
            new_desc = prompt(self.question_modif_desc)
            SceneService().modifier_desc_scene(
                scene=Session().scene_to_param, new_desc=new_desc["modif desc"], schema="ProjetInfo"
            )
            print(Fore.GREEN + "Modification effectuée avec succès" + Style.RESET_ALL)

        from view.view_param.menuparamsceneview import MenuParamSceneView

        return MenuParamSceneView()

    def display_info(self):
        print(Fore.BLUE + " [PARAMETRAGE] MENU SCENE ".center(80, "=") + Style.RESET_ALL)
