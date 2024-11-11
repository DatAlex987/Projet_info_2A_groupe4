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
                "message": "Que souhaitez-vous faire ? \n"
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
        self.questions_creation_scene = [
            {
                "type": "input",
                "name": "nom",
                "message": "Quel sera le nom de votre scène ?",
            },
            {
                "type": "input",
                "name": "description",
                "message": "Quelle sera la description de votre scène ?",
            },
        ]

    def make_choice(self):
        choix = prompt(self.question_choix_scene)
        if choix["Choix Scene"] == "Retour au menu de choix des sound-decks":
            # Contraint de faire l'import ici pour éviter un circular import
            from view.menuparamsdview import MenuParamSDView

            next_view = MenuParamSDView()
            return next_view
        if choix["Choix Scene"] == "Supprimer la sound-deck":
            confirmation = prompt(self.question_choix_suppr_sd)
            if confirmation["confirm suppr sd"]:
                try:
                    # Le SD à supprimer est celui sur lequel le user à cliqué
                    sd_to_delete = Session().sd_to_param
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
                # Contraint de faire l'import ici pour éviter un circular import
                from view.menuparam_view import MenuParamView

                next_view = MenuParamView()
            else:
                next_view = MenuParamSceneView()
            return next_view
            # Contraint de faire l'import ici pour éviter un circular import
            # from view.menuparamsdview import MenuParamSDView

            # next_view = MenuParamSDView()
        if choix["Choix Scene"] == "Ajouter une scène":
            scene_creee_avec_succes = False
            while not scene_creee_avec_succes:
                try:
                    info_new_scene = prompt(self.questions_creation_scene)
                    if SceneService().creer_scene(
                        nom=info_new_scene["nom"],
                        description=info_new_scene["description"],
                        schema="ProjetInfo",
                    ):
                        print(
                            Fore.GREEN
                            + f"Scène '{info_new_scene['nom']}' créée avec succès"
                            + Style.RESET_ALL
                        )
                        scene_creee_avec_succes = True
                except ValueError as e:
                    print(
                        Fore.RED + f"Erreur lors de la création de la scène : {e}" + Style.RESET_ALL
                    )
            next_view = MenuParamSceneView()
            return next_view
        else:
            id_scene_select = choix["Choix Scene"].split()[1]
            Session().scene_to_param = SceneService().instancier_scene_par_id(
                id_scene=id_scene_select, schema="ProjetInfo"
            )
            from view.menuparamscenespecifiqueview import MenuParamSceneSpecifiqueView

            next_view = MenuParamSceneSpecifiqueView()
        return next_view

    def display_info(self):
        print(Fore.BLUE + " MENU DE PARAMETRAGE ".center(80, "=") + Style.RESET_ALL)
