from colorama import Fore, Style
from InquirerPy import prompt

####
from service.scene_service import SceneService
from service.session import Session

####
from view.abstractview import AbstractView


class MenuJeuSceneView(AbstractView):
    "classe représentant l'accès au menu sound-deck, après le menu jeu"

    def __init__(self):
        super().__init__()

        self.question_choix_scene = [
            {
                "type": "list",
                "name": "Choix Scene",
                "message": "Quelle scène souhaitez-vous lancer ? \n"
                " ID         |   Nom   | Date de création \n"
                "------------------------------------------------------------",
                "choices": SceneService().formatage_question_scenes_of_sd_menu_jeu(),
            }
        ]

    def make_choice(self):
        choix = prompt(self.question_choix_scene)
        if choix["Choix Scene"] == "Retour au menu de choix des sound-decks":
            from view.view_jeu.menu_jeu_view import MenuJeuView

            next_view = MenuJeuView()
        else:
            id_scene_select = choix["Choix Scene"].split()[1]
            Session().scene_to_play = SceneService().instancier_scene_par_id(
                id_scene=id_scene_select, schema="ProjetInfo"
            )
            SceneService().jouer_scene(scene=Session().scene_to_play)
            next_view = MenuJeuSceneView()
        return next_view

    def display_info(self):
        print(Fore.BLUE + " [JEU] MENU SCENE ".center(80, "=") + Style.RESET_ALL)
