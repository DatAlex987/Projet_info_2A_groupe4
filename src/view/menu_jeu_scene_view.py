from colorama import Fore, Style
from InquirerPy import prompt

####
from service.user_service import UserService
from service.sd_service import SDService
from service.scene_service import SceneService

####
from view.abstractview import AbstractView
from view.menu_jeu_sons_view import MenuJeuSonsView
from view.session import Session


class MenuJeuSceneView(AbstractView):
    "classe représentant l'accès au menu sound-deck, après le menu principal"

    def __init__(self):
        super().__init__()

        self.question_choix_scene = [
            {
                "type": "list",
                "name": "Choix Scene",
                "message": "Quelle scène souhaitez-vous lancer ? \n"
                " ID         |   Nom   | Date de création \n"
                "------------------------------------------------------------",
                "choices": SceneService().formatage_question_scenes_of_sd_menu_jeu(
                    id_sd=Session().sd_to_param.id_sd
                ),
            }
        ]

    def make_choice(self):
        choix = prompt(self.question_choix_scene)
        if choix["Choix Scene"] == "Retour au menu de choix des sound-decks":
            from view.menu_jeu_view import MenuJeuView

            next_view = MenuJeuView()
        else:
            id_sd_select = choix["Choix Scene"].split()[1]
            Session().sd_to_param = SDService().instancier_sd_par_id(
                id_sd=id_sd_select, schema="ProjetInfo"
            )
            next_view = MenuJeuSonsView()
        return next_view

    def display_info(self):
        print(Fore.BLUE + " MENU DES SCENES [JEU] ".center(80, "=") + Style.RESET_ALL)
