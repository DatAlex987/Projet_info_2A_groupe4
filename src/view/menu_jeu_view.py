from view.abstractview import AbstractView
from colorama import Fore, Style
from InquirerPy import prompt

####
from service.user_service import UserService
from service.sd_service import SDService
from service.scene_service import SceneService

####
from view.abstractview import AbstractView
from view.session import Session
from view.menu_jeu_scene_view import MenuJeuSceneView


class MenuJeuView(AbstractView):
    "classe représentant l'accès au menu jeu, après le menu principal"

    def __init__(self):
        super().__init__()
        self.question = [
            {
                "type": "list",
                "name": "Choix SD",
                "message": "Quelle Sound-deck souhaitez vous jouer ? \n"
                " ID   |      Nom       |      Description               | Date de création \n"
                "----------------------------------------------------------------------------------",
                "choices": SDService().formatage_question_sds_of_user_menu_jeu(),
            }
        ]

    def make_choice(self):
        choix = prompt(self.question)
        if choix["Choix SD"] == "Retour au menu principal":
            from view.menuprincipalview import MenuPrincipalView

            next_view = MenuPrincipalView()

        else:
            id_sd_select = choix["Choix SD"].split()[1]
            Session().sd_to_play = SDService().instancier_sd_par_id(
                id_sd=id_sd_select, schema="ProjetInfo"
            )
            next_view = MenuJeuSceneView()
        return next_view

    def display_info(self):
        print(Fore.BLUE + " MENU DE JEU ".center(80, "=") + Style.RESET_ALL)
