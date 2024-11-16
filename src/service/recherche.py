from utils.singleton import Singleton
from InquirerPy import prompt
from service.freesound import Freesound
from service.session import Session
from business_object.son import Son
from colorama import Fore, Style
from rich.console import Console
from rich.table import Table
from rich.style import Style


class Recherche(metaclass=Singleton):

    def __init__(self):
        self.dict_critere = {}  # Dictionnaire pour stocker les critères de recherche
        self.limit = 10  # Limite par défaut pour le nombre de résultats
        self.results = []  # Stocke les résultats de recherche pour la pagination
        self.page_size = 5  # Nombre de résultats par page
        self.page = 1

    def ajouter_critere(self, reponse_critere):
        """Ajouter un critère de recherche au dictionnaire des critères."""
        if reponse_critere["tag"]:
            self.dict_critere["query"] = reponse_critere["tag"]
        if reponse_critere["duration_min"]:
            self.dict_critere["min_duration"] = reponse_critere["duration_min"]
        if reponse_critere["duration_max"]:
            self.dict_critere["max_duration"] = reponse_critere["duration_max"]
        if reponse_critere["limit"]:
            self.limit = int(reponse_critere["limit"])
        return True

    def reinitialiser_criteres(self):
        """Réinitialise les critères de recherche."""
        self.dict_critere.clear()
        self.limit = 10
        return True

    def formatage_choix_resultats_recherche(self):
        start = self.page * self.page_size
        end = start + self.page_size
        page_results = self.results[start:end]
        choices = []
        for idx, son in enumerate(page_results):
            choices.append(
                {"name": f"{idx + 1}. ID: {son['id']}, Nom: {son['name']}", "value": son}
            )
        if self.page > 0:
            choices.insert(0, "Page précédente")
        if self.page <= round(len(self.results) / self.page_size, 0) - 1:
            choices.append("Page suivante")
        choices.append("Retour au menu de recherche")
        return choices

    def lancer_recherche(self):
        """Exécute la recherche sur Freesound en fonction des critères sélectionnés."""
        self.page = 1
        if "query" in self.dict_critere:
            try:
                self.results = Freesound.rechercher_multi_filtres(
                    dico_filtres=self.dict_critere, limit=self.limit
                )
                if self.results:
                    self.page = 0  # Set the initial page to 0
                    return self.results
            except Exception as e:
                print(f"Erreur lors de la recherche : {e}")

    def afficher_details_son(self, son):
        """Affiche les détails d'un son"""
        try:
            son_id = str(son["id"])
            son_details = Freesound.rechercher_par_id(
                id=son_id
            )  # Nouvelle requête pour obtenir les détails du son
            Session().son_to_dl = son_details
        except Exception as e:
            print(f"Erreur lors de la récupération des détails du son : {e}")
            return

        # Création d'une instance de Console pour afficher les informations
        console = Console()

        # Formatage de la durée et de la taille du fichier
        duree_formatee = (
            f"{int(son_details['duration'] // 60)} min {int(son_details['duration'] % 60)} sec"
        )
        poids_formate = f"{son_details['filesize'] / (1024 * 1024):.2f} Mo"

        # Création du tableau avec les détails du son
        table = Table(
            show_header=True,
            header_style=Style(color="chartreuse1", bold=True),
            title="--------------- Détails du Son ---------------",
            style="white",
        )

        # Définition de l'alignement centré et de la couleur bleue pour les titres des colonnes
        table.add_column("Champ", style=Style(color="honeydew2"), width=20)
        table.add_column("Détails", style=Style(color="honeydew2"))

        # Ajout des informations du son dans le tableau
        table.add_row("ID Freesound", str(son_details["id"]))
        table.add_row("Nom", son_details["name"])
        table.add_row("Tags", ", ".join(son_details["tags"][:5]))  # Afficher les 5 premiers tags
        table.add_row("Format", son_details["type"])
        table.add_row("Durée", duree_formatee)
        table.add_row("Taille", poids_formate)

        # Affichage du tableau dans la console
        console.print(table)
