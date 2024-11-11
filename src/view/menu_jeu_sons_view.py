from colorama import Fore, Style
from InquirerPy import prompt

####
from service.user_service import UserService
from service.sd_service import SDService
from service.scene_service import SceneService
from service.son_service import SonService

####
from view.abstractview import AbstractView
from view.session import Session


class MenuJeuSonsView(AbstractView):
    "classe représentant l'accès au menu des sons, après le menu des scènes"

    def __init__(self):
        super().__init__()

        self.question_choix_son = [
            {
                "type": "list",
                "name": "Choix Son",
                "message": "Sélectionnez un son pour l'enclencher ou l'arrêter \n"
                "  Type        |   Nom   | ID Freesound | Déclenchement | Etat \n"
                "------------------------------------------------------------",
                "choices": SonService().formatage_question_sons_of_scene_menu_jeu(
                    id_sd=Session().sd_to_param.id_sd, id_scene=Session().scene_to_param.id_scene
                ),
            }
        ]

    def make_choice(self):
        choix = prompt(self.question_choix_son)
        if choix["Choix Son"] == "Retour au menu de choix des scènes":
            from view.menu_jeu_scene_view import MenuJeuSceneView

            next_view = MenuJeuSceneView()
        else:
            id_scene_select = choix["Choix Son"].split()[1]
            Session().scene_to_param = SDService().instancier_scene_par_id(
                id_scene=id_scene_select, schema="ProjetInfo"
            )
            # next_view = MenuJeuSonsView() : remplacer par juste modifier le déclencher
        return next_view

    def display_info(self):
        print(Fore.BLUE + " MENU DES SONS [JEU] ".center(80, "=") + Style.RESET_ALL)
