from rich.console import Console
from InquirerPy import prompt
from view.abstractview import AbstractView
from view.session import Session
from view.view_jeu.menu_jeu_scene_view import MenuJeuSceneView
from service.sd_service import SDService
from colorama import Fore, Style
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.box import DOUBLE  # Importer le bon type de boîte


class MenuJeuView(AbstractView):
    def __init__(self):
        super().__init__()
        self.sd_service = SDService()
        self.console = Console()

    def make_choice(self):
        # Affiche le tableau des Sounddecks
        tableau = self.sd_service.afficher_tableau_sds_user()
        self.console.print(tableau)

        # Crée la liste des choix pour InquirerPy
        choices = self.sd_service.obtenir_choices_sds_user()
        choices.append("Retour au menu principal")

        question = [
            {
                "type": "list",
                "name": "Choix SD",
                "message": "Veuillez sélectionner une Sound-deck (ou revenir au menu principal) :",
                "choices": choices,
            }
        ]

        choix = prompt(question)
        if choix["Choix SD"] == "Retour au menu principal":
            from view.menuprincipalview import MenuPrincipalView

            next_view = MenuPrincipalView()
        else:
            # Extraire l'ID de la Sounddeck sélectionnée
            id_sd_select = choix["Choix SD"].split()[1]
            Session().sd_to_play = self.sd_service.instancier_sd_par_id(
                id_sd=id_sd_select, schema="ProjetInfo"
            )
            next_view = MenuJeuSceneView()
        return next_view

    def display_info(self):
        print(Fore.BLUE + " MENU DE JEU ".center(80, "=") + Style.RESET_ALL)
