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
        self.question_choix_suppr_sd = [
            {
                "type": "confirm",
                "name": "confirm suppr sd",
                "message": "Etes-vous sûr de vouloir supprimer votre sound-deck ? Sa suppression entraînera la perte de tout ce qu'elle contient.",
            }
        ]

    def make_choice(self):
        choix = prompt(self.question_choix_scene)
        if choix["Choix Scene"] == "Retour au menu de paramétrage":
            # Contraint de faire l'import ici pour éviter un circular import
            from view.menuparam_view import MenuParamView

            next_view = MenuParamView()
        if choix["Choix Scene"] == "Supprimer la sound-deck":
            confirmation = prompt(self.question_choix_suppr_sd)
            if confirmation["confirm suppr sd"]:
                try:
                    sd_to_delete = (
                        Session().sd_to_param
                    )  # Le SD à supprimer est celui sur lequel le user à cliqué
                    if SDService().supprimer_sd(
                        sd=sd_to_delete,
                        schema="ProjetInfo",
                    ):
                        print(
                            Fore.GREEN
                            + f"Sound-deck '{Session().sd_to_param.nom}' supprimée avec succès"
                            + Style.RESET_ALL
                        )

                except (ValueError, AttributeError) as e:
                    print(
                        Fore.RED
                        + f"Erreur lors de la suppression de la Sound-deck : {e}"
                        + Style.RESET_ALL
                    )
                    next_view = MenuParamSceneView()
            # Contraint de faire l'import ici pour éviter un circular import
            from view.menuparamsdview import MenuParamSDView

            next_view = MenuParamSDView()
        if choix["Choix Scene"] == "Ajouter une scène":
            pass
        else:
            id_scene_select = choix["Choix Scene"].split()[1]  # A VERIFIER

            from view.menuparam_view import MenuParamView

            next_view = MenuParamView()
        return next_view

    def display_info(self):
        print(Fore.BLUE + " MENU DE PARAMETRAGE ".center(80, "=") + Style.RESET_ALL)
