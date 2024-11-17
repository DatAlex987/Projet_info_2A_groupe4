from colorama import Fore, Style
from InquirerPy import prompt
import re

####
# from service.user_service import UserService
from service.sd_service import SDService

# from service.scene_service import SceneService
from service.son_service import SonService

####
from view.abstractview import AbstractView
from service.session import Session


class MenuConsulterSonsView(AbstractView):
    "classe représentant l'accès au menu des sons, après le menu des scènes"

    def __init__(self):
        super().__init__()

        self.question_choix_son = [
            {
                "type": "list",
                "name": "Choix Son",
                "message": "Sélectionnez un son pour l'enclencher ou l'arrêter \n"
                "  Type        |   Nom   | ID Freesound | ID du son | Déclenchement | Etat \n"
                "------------------------------------------------------------",
                "choices": SonService().formatage_question_sons_of_scene_menu_jeu(
                    id_sd=Session().sd_to_consult.id_sd,
                    id_scene=Session().scene_to_consult.id_scene,
                ),
            }
        ]

    def make_choice(self):  # voir avec alex : jouer son
        choix = prompt(self.question_choix_son)
        if choix["Choix Son"] == "Retour au menu de choix des scènes":
            from view.view_consulter_user.consulter_scene_view import ConsulterSceneView

            next_view = ConsulterSceneView()
        else:
            id_son_striped = choix["Choix Son"].split("|")[0].split(". ")[1].strip()
            type_son = re.search(r"\[(.*?)\]", choix["Choix Son"]).group(1)
            Session().son_to_consult = SDService().instancier_son_par_id_type(
                id_son=id_son_striped, type_son=type_son, schema="ProjetInfo"
            )
            # next_view = MenuJeuSonsView() : remplacer par juste modifier le déclencher
        return next_view

    def display_info(self):
        print(Fore.BLUE + " [JEU] MENU SON ".center(80, "=") + Style.RESET_ALL)