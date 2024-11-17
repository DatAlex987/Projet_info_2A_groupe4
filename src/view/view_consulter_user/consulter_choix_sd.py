from view.abstractview import AbstractView
from colorama import Fore, Style
from InquirerPy import prompt

####
from service.user_service import UserService
from service.sd_service import SDService

####
from view.abstractview import AbstractView
from view.session import Session

# from view.view_consulter_user.menu_consulter_createur_view import ConsulterCreateurView
# from view.view_consulter_user.menu_consulter_nom_view import ConsulterNomView


class ConsulterChoixSD(AbstractView):

    def __init__(self):
        super().__init__()
        self.question = [
            {
                "type": "list",
                "name": "Choix SD",
                "message": ("Que souhaitez-vous faire avec la Sound-deck ? \n"),
                "choices": [
                    "Découvrir la SD",
                    "Sauvegarder la SD dans ma bibliothèque",
                    "Dupliquer cette SD dans ma bibliothèque",
                    "Retour au menu précédent",
                ],
            }
        ]

    def make_choice(self):
        choix = prompt(self.question)
        if choix["Choix SD"] == "Découvrir la SD":
            from view.view_consulter_user.consulter_scene_view import ConsulterSceneView

            next_view = ConsulterSceneView()
        if choix["Choix SD"] == "Sauvegarder la SD dans ma bibliothèque":
            pass  # à faire
        if choix["Choix SD"] == "Dupliquer cette SD dans ma bibliothèque":
            pass  # à faire
        if choix["Choix SD"] == "Retour au menu précédent":
            from view.view_consulter_user.consulter_sds_view import ConsulterSDsView

            next_view = ConsulterSDsView()

        return next_view

    def display_info(self):
        print(Fore.BLUE + " [JEU] MENU SOUND-DECK ".center(80, "=") + Style.RESET_ALL)
