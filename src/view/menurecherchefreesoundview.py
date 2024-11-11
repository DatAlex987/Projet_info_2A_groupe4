"""Ce module implémente la view dédiée à la recherche de sons sur Freesound"""

from colorama import Fore, Style
from InquirerPy import prompt
from view.abstractview import AbstractView
from view.session import Session
from service.sd_service import SDService
from service.scene_service import SceneService
from service.freesound import Freesound


class MenuRechercheFreesoundView(AbstractView):
    """Classe représentant la view de recherche de sons sur Freesound"""

    def __init__(self):
        super().__init__()
        self.questions = [
            {
                "type": "list",
                "name": "Menu recherche",
                "message": "Que voulez-vous faire ?",
                "choices": [
                    "Ajouter un critère de recherche",
                    "Réinitialiser les critères",
                    "Lancer la recherche",
                    "Quitter le menu recherche",
                ],
            }
        ]
        self.dict_critere = {}  # Dictionnaire pour stocker les critères de recherche
        self.limit = 10  # Limite par défaut pour le nombre de résultats
        self.results = []  # Stocke les résultats de recherche pour la pagination
        self.page_size = 5  # Nombre de résultats par page

    def make_choice(self):
        while True:
            choix = prompt(self.questions)["Menu recherche"]

            if choix == "Ajouter un critère de recherche":
                self.ajouter_critere()
            elif choix == "Réinitialiser les critères":
                self.reinitialiser_criteres()
            elif choix == "Lancer la recherche":
                self.lancer_recherche()
            elif choix == "Quitter le menu recherche":
                print("Retour au menu principal.")
                break

    def ajouter_critere(self):
        """Ajouter un critère de recherche au dictionnaire des critères."""
        question_critere = [
            {
                "type": "input",
                "name": "tag",
                "message": "Entrez un tag pour la recherche de sons :",
            },
            {
                "type": "input",
                "name": "limit",
                "message": f"Combien de résultats voulez-vous pouvoir consulter ? (actuel: {self.limit}) :",
                "validate": lambda val: val.isdigit() and int(val) > 0,
            },
        ]
        reponse_critere = prompt(question_critere)
        if reponse_critere["tag"]:
            self.dict_critere["tag"] = reponse_critere["tag"]
        if reponse_critere["limit"]:
            self.limit = int(reponse_critere["limit"])

        print("Critère ajouté : ", self.dict_critere)

    def reinitialiser_criteres(self):
        """Réinitialise les critères de recherche."""
        self.dict_critere.clear()
        self.limit = 10
        print("Critères de recherche réinitialisés.")

    def lancer_recherche(self):
        """Exécute la recherche sur Freesound en fonction des critères sélectionnés."""
        if "tag" in self.dict_critere:
            try:
                self.results = Freesound.rechercher_par_tag(
                    tag=self.dict_critere["tag"], limit=self.limit
                )
                if self.results:
                    self.page = 0  # Set the initial page to 0
                    self.afficher_resultats()  # No need for page argument
                else:
                    print("Aucun son trouvé avec les critères de recherche.")
            except Exception as e:
                print(f"Erreur lors de la recherche : {e}")
        else:
            print("Aucun critère spécifié pour la recherche. Veuillez ajouter un critère.")

    def afficher_resultats(self):
        """Affiche les résultats de recherche par pages de 5 et gère les sélections."""
        self.page_size = 5

        while True:
            start = self.page * self.page_size
            end = start + self.page_size
            page_results = self.results[start:end]

            choices = [
                {"name": f"{idx + 1}. ID: {son['id']}, Nom: {son['name']}", "value": son}
                for idx, son in enumerate(page_results)
            ]
            if self.page > 0:
                choices.insert(0, {"name": "Page précédente", "value": "previous"})
            if end < len(self.results):
                choices.append({"name": "Page suivante", "value": "next"})
            choices.append({"name": "Retour au menu de recherche", "value": "quit"})

            question = [
                {
                    "type": "list",
                    "name": "choix_resultat",
                    "message": "Sélectionnez un son ou naviguez dans les pages :",
                    "choices": choices,
                }
            ]
            choix = prompt(question)["choix_resultat"]

            if choix == "next":
                self.page += 1
            elif choix == "previous":
                self.page -= 1
            elif choix == "quit":
                break
            else:
                self.afficher_details_son(choix)  # Pass selected sound to details view

    def afficher_details_son(self, son):
        """Affiche les détails d'un son avec des options pour écouter, sauvegarder, ou retourner aux résultats."""
        # Fetch more details using the ID of the sound
        try:
            son_id = str(son["id"])
            son_details = Freesound.rechercher_par_id(id=son_id)  # New request to get full details
        except Exception as e:
            print(f"Erreur lors de la récupération des détails du son : {e}")
            return

        # Display detailed information after successful retrieval
        while True:
            print(Fore.YELLOW + f"\nDétails du Son - {son_details['name']}\n" + Style.RESET_ALL)
            print(f"ID: {son_details['id']}")
            print(f"Nom: {son_details['name']}")
            print(f"Tags: {', '.join(son_details['tags'])}")
            print(f"Licence: {son_details['license']}")
            print(f"Créateur: {son_details['username']}")
            print(f"Durée: {son_details.get('duration', 'Non disponible')} secondes")
            print(f"Taille du fichier: {son_details.get('filesize', 'Non disponible')} octets")
            print(f"Type: {son_details.get('type', 'Non disponible')}")
            # Add more fields here if available in the son_details response

            question = [
                {
                    "type": "list",
                    "name": "action",
                    "message": "Que voulez-vous faire ?",
                    "choices": [
                        "Écouter le son",
                        "Sauvegarder dans la scène",
                        "Retour aux résultats de recherche",
                    ],
                }
            ]
            action = prompt(question)["action"]

            if action == "Écouter le son":
                url_mp3 = son_details.get("previews", {}).get("preview-hq-mp3")
                if url_mp3:
                    print(
                        f"Lecture du son : {url_mp3}"
                    )  # Replace with actual playback functionality
                else:
                    print("Aucun aperçu disponible pour ce son.")
            elif action == "Sauvegarder dans la scène":
                SceneService.save_sound_to_scene(son_details)
                print("Son sauvegardé dans la scène.")
            elif action == "Retour aux résultats de recherche":
                break

    def display_info(self):
        print(Fore.BLUE + " MENU DE RECHERCHE ".center(80, "=") + Style.RESET_ALL)
