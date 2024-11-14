"""Ce module implémente la view dédiée au paramétrage d'une scène' de l'utilisateur"""

from colorama import Fore, Style
from InquirerPy import prompt
from view.abstractview import AbstractView
from view.session import Session
from service.sd_service import SDService
from service.scene_service import SceneService
from service.son_service import SonService
from view.menurecherchefreesoundview import MenuRechercheFreesoundView


class MenuParamSceneSpecifiqueView(AbstractView):
    """Classe représentant la view de paramétrage d'une scène'"""

    def __init__(self):
        super().__init__()

        self.question_choix_scene_specifique = [
            {
                "type": "list",
                "name": "Choix Scene Specifique",
                "message": "Que souhaitez-vous faire (Sélectionnez un son pour le modifier) ? \n"
                " ID Freesound  |    Type      |   Nom   |   Durée \n"
                "------------------------------------------------------------",
                "choices": SonService().formatage_question_sons_of_scene(
                    id_sd=Session().sd_to_param.id_sd, id_scene=Session().scene_to_param.id_scene
                ),
            }
        ]
        self.question_choix_suppr_scene = [
            {
                "type": "confirm",
                "name": "confirm suppr scene",
                "message": "Etes-vous sûr de vouloir supprimer votre scène ? Sa suppression entraînera la perte de tout ce qu'elle contient.",
            }
        ]

    def make_choice(self):
        choix = prompt(self.question_choix_scene_specifique)
        if choix["Choix Scene Specifique"] == "Retour au menu de choix des scènes":
            # Contraint de faire l'import ici pour éviter un circular import
            from view.menuparamsceneview import MenuParamSceneView

            next_view = MenuParamSceneView()
            return next_view
        if choix["Choix Scene Specifique"] == "Supprimer la scène":
            confirmation = prompt(self.question_choix_suppr_scene)
            if confirmation["confirm suppr scene"]:
                try:
                    # La scène à supprimer est celle sur lequel le user à cliqué
                    scene_to_delete = Session().scene_to_param
                    if SceneService().supprimer_scene(
                        scene=scene_to_delete,
                        schema="ProjetInfo",
                    ):
                        print(
                            Fore.GREEN
                            + f"Scène '{Session().scene_to_param.nom}' supprimée avec succès"
                            + Style.RESET_ALL
                        )

                except (ValueError, AttributeError) as e:
                    print(
                        Fore.RED
                        + f"Erreur lors de la suppression de la scène : {e}"
                        + Style.RESET_ALL
                    )
                # Contraint de faire l'import ici pour éviter un circular import
                from view.menuparamsceneview import MenuParamSceneView

                next_view = MenuParamSceneView()
            else:
                from view.menuparamsceneview import MenuParamSceneView

                next_view = MenuParamSceneView()
            return next_view
        if choix["Choix Scene Specifique"] == "Ajouter un son via Freesound":
            return MenuRechercheFreesoundView()
        else:
            # choisir un son
            print("print de la ligne choisie", choix["Choix Scene Specifique"])
            id_freesound = choix["Choix Scene Specifique"].split("|")[0].split(". ")[1].strip()
            print("id son striped:", id_freesound)
            id_scene_select = choix["Choix Scene"].split()[1]
            Session().scene_to_param = SceneService().instancier_scene_par_id(
                id_scene=id_scene_select, schema="ProjetInfo"
            )
            from view.menuparamscenespecifiqueview import MenuParamSceneSpecifiqueView

            next_view = MenuParamSceneSpecifiqueView()
        return next_view

    def display_info(self):
        print(Fore.BLUE + " MENU DE PARAMETRAGE ".center(80, "=") + Style.RESET_ALL)