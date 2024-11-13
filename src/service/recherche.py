from utils.singleton import Singleton
from InquirerPy import prompt
from service.freesound import Freesound
from view.session import Session
from business_object.son import Son
from colorama import Fore, Style


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
            self.dict_critere["tag"] = reponse_critere["tag"]
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
        if "tag" in self.dict_critere:
            try:
                self.results = Freesound.rechercher_par_tag(
                    tag=self.dict_critere["tag"], limit=self.limit
                )
                if self.results:
                    self.page = 0  # Set the initial page to 0
                    return self.results
            except Exception as e:
                print(f"Erreur lors de la recherche : {e}")

    def afficher_details_son(self, son):
        """Affiche les détails dun son avec des options pour écouter, sauvegarder, ou retourner aux résultats."""
        # Fetch more details using the ID of the sound
        try:
            son_id = str(son["id"])
            son_details = Freesound.rechercher_par_id(id=son_id)  # New request to get full details
        except Exception as e:
            print(f"Erreur lors de la récupération des détails du son : {e}")
            return

        # Display detailed information after successful retrieval
        duree_formatee = (
            f"{int(son_details['duration'] // 60)}min{int(son_details['duration'] % 60)}sec"
        )
        poids_formate = f"{son_details['filesize'] / (1024 * 1024):.2f}Mo"
        display = f"""
        ================Détails du Son================\n
        ID Freesound: {son_details["id"]}
        Nom: {son_details["name"]}
        Tags: {son_details["tags"][:5]}
        ============INFORMATIONS TECHNIQUES===========
        Format du fichier: {son_details["type"]}
        Durée: {duree_formatee}
        Taille du fichier: {poids_formate}"""

        print(display)
