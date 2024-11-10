"""Ce module implémente la view dédiée au paramétrage des SD de l'utilisateur"""

from colorama import Fore, Style
from InquirerPy import prompt
from view.abstractview import AbstractView
from view.session import Session
from service.sd_service import SDService
from service.scene_service import SceneService


class MenuParamSceneView(AbstractView):
    """Classe représentant la view de paramétrage des Sound-deck"""

    def __init__(self):
        super().__init__()

        self.question_choix_scene = [
            {
                "type": "list",
                "name": "Choix Scene",
                "message": "Que souhaitez-vous faire ? ? \n"
                " ID         |   Nom   | Date de création \n"
                "------------------------------------------------------------",
                "choices": SceneService().formatage_question_scenes_of_sd(
                    id_sd=Session().sd_to_param.id_sd
                ),
            }
        ]

    def make_choice(self):
        choix = prompt(self.question_choix_scene)
        if choix["Choix Scene"] == "Retour au menu de paramétrage":
            # Contraint de faire l'import ici pour éviter un circular import
            from view.menuparam_view import MenuParamView

            next_view = MenuParamView()
        if choix["Choix Scene"] == "Supprimer la sound-deck":
            sd_supprimee_avec_succes = False
            while not sd_supprimee_avec_succes:
                try:
                    if SDService().supprimer_sd(
                        id_sd=Session().sd_to_param.id_sd,
                        schema="ProjetInfo",
                    ):  # apres to modify
                        pass
                    """
                        print(
                            Fore.GREEN
                            + f"Sound-deck '{infos_creation_sd['nom']}' créée avec succès"
                            + Style.RESET_ALL
                        )
                        next_view = MenuParamView()
                        sd_creee_avec_succes = True
                        """
                except ValueError as e:
                    """
                    print(
                        Fore.RED
                        + f"Erreur lors de la création de la Sound-deck : {e}"
                        + Style.RESET_ALL
                    )
                    """
            next_view = MenuParamSceneView()

        else:
            id_scene_select = choix["Choix Scene"].split()[1]  # A VERIFIER
            print(id_scene_select)

            from view.menuparam_view import MenuParamView

            next_view = MenuParamView()
        return next_view

    def display_info(self):
        print(Fore.BLUE + " MENU DE PARAMETRAGE ".center(80, "=") + Style.RESET_ALL)
