from colorama import Fore, Style
from InquirerPy import prompt

####
from service.sd_service import SDService

####
from view.abstractview import AbstractView


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
                    "Sauvegarder la SD dans ma bibliothèque (modifications impossibles)",
                    "Dupliquer cette SD dans ma bibliothèque (modifications possibles)",
                    "Retour au menu précédent",
                ],
            }
        ]

    def make_choice(self):
        choix = prompt(self.question)
        if choix["Choix SD"] == "Découvrir la SD":
            from view.view_consulter_user.consulter_scene_view import ConsulterSceneView

            next_view = ConsulterSceneView()
        if (
            choix["Choix SD"]
            == "Sauvegarder la SD dans ma bibliothèque (modifications impossibles)"
        ):
            SDService().ajouter_sd_existante_to_user(schema="ProjetInfo")
            print(
                Fore.GREEN
                + "Sauvegarde de la sound-deck dans votre biliothèque avec succès"
                + Style.RESET_ALL
            )
            from view.view_consulter_user.consulter_sds_view import ConsulterSDsView

            return ConsulterSDsView()
        if choix["Choix SD"] == "Dupliquer cette SD dans ma bibliothèque (modifications possibles)":
            SDService().dupliquer_sd_existante_to_user(schema="ProjetInfo")
            print(
                Fore.GREEN
                + "Duplication de la sound-deck dans votre biliothèque avec succès"
                + Style.RESET_ALL
            )
            from view.view_consulter_user.consulter_sds_view import ConsulterSDsView

            return ConsulterSDsView()
        if choix["Choix SD"] == "Retour au menu précédent":
            from view.view_consulter_user.consulter_sds_view import ConsulterSDsView

            next_view = ConsulterSDsView()

        return next_view

    def display_info(self):
        print(Fore.BLUE + " [JEU] MENU SOUND-DECK ".center(80, "=") + Style.RESET_ALL)
