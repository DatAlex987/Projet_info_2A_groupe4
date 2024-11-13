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
        self.etat_recherche = 1  # Si 0 : aucun son trouvé, si -1 : aucun critère renseigné
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

    def lancer_recherche(self):
        self.etat_recherche = 1
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
                    self.etat_recherche = 0
            except Exception as e:
                print(f"Erreur lors de la recherche : {e}")
        else:
            self.etat_recherche = -1

    def afficher_resultats(self):  # Page suivante non affichée après les 10 premiers résultats
        """Affiche les résultats de recherche par pages de 5 et gère les sélections."""
        self.page = 1
        while True:
            question = [
                {
                    "type": "list",
                    "name": "choix_resultat",
                    "message": "Sélectionnez un son ou naviguez dans les pages :",
                    "choices": self.formatage_choix_resultats_recherche(),
                }
            ]
            choix = prompt(question)["choix_resultat"]

            if choix == "Page suivante":
                self.page += 1
            elif choix == "Page précédente":
                self.page -= 1
            elif choix == "Retour au menu de recherche":
                break
            else:
                self.afficher_details_son(choix)  # Pass selected sound to details view

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
        Taille du fichier:{poids_formate}"""
        while True:
            print(display)

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
                pass  # Will be done later
            elif action == "Sauvegarder dans la scène":
                Session().son_to_dl = son_details
                # break
                from view.accueilview import AccueilView

                return AccueilView()
                question_type = [
                    {
                        "type": "list",
                        "name": "choix type",
                        "message": "Quel sera le type du son dans cette scène ?",
                        "choices": [
                            "Son manuel",
                            "Son aléatoire",
                            "Son continu",
                        ],
                    }
                ]
                type_voulu = prompt(question_type)
                if type_voulu["choix type"] == "Son manuel":
                    pass
                elif type_voulu["choix type"] == "Son aléatoire":
                    pass
                elif type_voulu["choix type"] == "Son continu":
                    pass
            elif action == "Retour aux résultats de recherche":
                break
