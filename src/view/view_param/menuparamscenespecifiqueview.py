"""Ce module implémente la view dédiée au paramétrage d'une scène' de l'utilisateur"""

from colorama import Fore, Style
from InquirerPy import prompt
import re

####
# from service.sd_service import SDService
from service.scene_service import SceneService
from service.son_service import SonService

####
from view.menurecherchefreesoundview import MenuRechercheFreesoundView
from view.view_param.menuparammodifsonview import MenuParamModifSonView
from view.abstractview import AbstractView
from view.session import Session


class MenuParamSceneSpecifiqueView(AbstractView):
    """Classe représentant la view de paramétrage d'une scène'"""

    def __init__(self):
        super().__init__()

        self.question_choix_suppr_scene = [
            {
                "type": "confirm",
                "name": "confirm suppr scene",
                "message": (
                    "Etes-vous sûr de vouloir supprimer votre scène ? "
                    "Sa suppression entraînera la perte de tout ce qu'elle contient."
                ),
            }
        ]

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

    def make_choice(self):
        choix = prompt(self.question_choix_scene_specifique)
        if choix["Choix Scene Specifique"] == "Retour au menu de choix des scènes":
            # Contraint de faire l'import ici pour éviter un circular import
            from view.view_param.menuparamsceneview import MenuParamSceneView

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
                from view.view_param.menuparamsceneview import MenuParamSceneView

                next_view = MenuParamSceneView()
            else:
                from view.view_param.menuparamsceneview import MenuParamSceneView

                next_view = MenuParamSceneView()
            return next_view
        if choix["Choix Scene Specifique"] == "Ajouter un son via Freesound":
            return MenuRechercheFreesoundView()
        else:
            # On extrait l'id du son sélectionné ainsi que son type
            id_freesound_striped = (
                choix["Choix Scene Specifique"].split("|")[0].split(". ")[1].strip()
            )
            type_son = re.search(r"\[(.*?)\]", choix["Choix Scene Specifique"]).group(1)
            # Puis on update la session
            Session().son_to_param = SonService().instancier_son_par_id_type(
                id_freesound=id_freesound_striped, type_son=type_son, schema="ProjetInfo"
            )
            next_view = MenuParamModifSonView()
        return next_view

    def display_info(self):
        print(Fore.BLUE + " MENU DE PARAMETRAGE ".center(80, "=") + Style.RESET_ALL)
