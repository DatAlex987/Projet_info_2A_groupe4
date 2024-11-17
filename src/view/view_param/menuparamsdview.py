"""Ce module implémente la view dédiée au paramétrage des SD de l'utilisateur"""

from colorama import Fore, Style
from InquirerPy import prompt

####
from service.sd_service import SDService

# from service.scene_service import SceneService

####
from view.abstractview import AbstractView
from service.session import Session
from view.view_param.menuparamsceneview import MenuParamSceneView


class MenuParamSDView(AbstractView):
    """Classe représentant la view de paramétrage des Sound-deck"""

    def __init__(self):
        super().__init__()
        self.question = [
            {
                "type": "list",
                "name": "Choix SD",
                "message": (
                    "Quelle Sound-deck souhaitez-vous modifier ? \n"
                    " ID   |      Nom       |    Description               "
                    "| Date de création \n"
                    "-------------------------------------------------------------"
                    "---------------------"
                ),
                "choices": SDService().formatage_question_sds_of_user(),
            }
        ]

    def make_choice(self):
        choix = prompt(self.question)
        if choix["Choix SD"] == "Retour au menu de paramétrage":
            from view.view_param.menuparam_view import MenuParamView

            next_view = MenuParamView()
        else:
            id_sd_select = choix["Choix SD"].split()[1]
            Session().sd_to_param = SDService().instancier_sd_par_id(
                id_sd=id_sd_select, schema="ProjetInfo"
            )
            if not Session().utilisateur.id_user == Session().sd_to_param.id_createur:
                print(
                    Fore.RED
                    + "Cette sound-deck ne vous appartient pas, vous ne pouvez pas la modifier"
                    + Style.RESET_ALL
                )
                return MenuParamSDView()
            next_view = MenuParamSceneView()
        return next_view

    def display_info(self):
        print(Fore.BLUE + " [PARAMETRAGE] MENU SOUND-DECK ".center(80, "=") + Style.RESET_ALL)
