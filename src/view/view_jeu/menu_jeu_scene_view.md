# menu_jeu_scene_view.py
# from colorama import Style
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.box import DOUBLE  # Importer le bon type de boîte
from InquirerPy import prompt

# Importation des services et classes nécessaires
# from service.user_service import UserService

# from service.sd_service import SDService
from service.scene_service import SceneService

####
from view.abstractview import AbstractView
from view.view_jeu.menu_jeu_sons_view import MenuJeuSonsView
from view.session import Session


class MenuJeuSceneView(AbstractView):
    "classe représentant l'accès au menu sound-deck, après le menu jeu"

    def __init__(self):
        super().__init__()

        self.console = Console()

        # Initialisation des données pour la question des scènes
        self.question_choix_scene = [
            {
                "type": "list",
                "name": "Choix Scene",
                "message": (
                    f"Quelle scène de '{Session().sd_to_play.nom}' souhaitez-vous lancer ? \n"
                ),
                "choices": SceneService().formatage_question_scenes_of_sd_menu_jeu(
                    id_sd=Session().sd_to_play.id_sd
                ),
            }
        ]

    def make_choice(self):
        # Affichage du menu de choix
        choix = prompt(self.question_choix_scene)
        if choix["Choix Scene"] == "Retour au menu de choix des sound-decks":
            # Déplacer l'importation ici pour éviter l'import circulaire
            from view.view_jeu.menu_jeu_view import MenuJeuView  # Importation locale

            next_view = MenuJeuView()
        else:
            id_scene_select = choix["Choix Scene"].split()[1]
            Session().scene_to_play = SceneService().instancier_scene_par_id(
                id_scene=id_scene_select, schema="ProjetInfo"
            )
            next_view = MenuJeuSonsView()
        return next_view

    def display_info(self):
        # Création du tableau avec Rich
        table = Table(show_header=True, header_style="bold blue", box=DOUBLE)
        table.add_column("ID", justify="center")
        table.add_column("Nom", justify="left")
        table.add_column("Date de création", justify="center")

        sds_user = Session().utilisateur.SD_possedes
        sd_selectionne = None
        for sd in sds_user:
            if sd.id_sd == Session().sd_to_play.id_sd:
                sd_selectionne = sd
        compteur = 1
        for scene in sd_selectionne.scenes:
            table.add_row(str(compteur), scene.nom, str(scene.date_creation))
            compteur += 1

        # Ajouter une ligne pour "Retour au menu de choix des sound-decks"
        table.add_row("", "Retour au menu de choix des sound-decks", "", style="bold red")

        # Affichage du tableau dans un panneau pour une meilleure présentation
        self.console.print(Panel(table, title="Liste des scènes", border_style="green"))