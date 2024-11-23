from colorama import Fore, Style
from InquirerPy import prompt

####
from service.session import Session
from service.scene_service import SceneService

####
from view.abstractview import AbstractView


class ConsulterSceneView(AbstractView):
    "classe représentant l'accès au menu de consultation des scènes"

    def __init__(self):
        super().__init__()

        self.question_choix_scene = [
            {
                "type": "list",
                "name": "Choix Scene",
                "message": "Quelle scène souhaitez-vous lancer ? \n"
                " ID         |   Nom   | Date de création \n"
                "------------------------------------------------------------",
                "choices": SceneService().formatage_question_scenes_of_sd_menu_consult(),
            }
        ]

    def make_choice(self):
        choix = prompt(self.question_choix_scene)
        if choix["Choix Scene"] == "Retour au menu de choix des sound-decks":
            from view.view_consulter_user.consulter_sds_view import ConsulterSDsView

            next_view = ConsulterSDsView()
        else:
            id_scene_select = choix["Choix Scene"].split()[1]
            Session().scene_to_consult = SceneService().instancier_scene_par_id(
                id_scene=id_scene_select, schema="ProjetInfo"
            )
            from view.view_consulter_user.consulter_son_view import MenuConsulterSonsView

            next_view = MenuConsulterSonsView()
        return next_view

    def display_info(self):
        print(Fore.BLUE + " [JEU] MENU SCENE ".center(80, "=") + Style.RESET_ALL)
