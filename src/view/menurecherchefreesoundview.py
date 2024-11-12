"""Ce module implémente la view dédiée à la recherche de sons sur Freesound"""

from colorama import Fore, Style
from InquirerPy import prompt
from view.abstractview import AbstractView
from view.session import Session
from service.sd_service import SDService
from service.scene_service import SceneService
from service.freesound import Freesound
from service.recherche import Recherche


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
        self.question_critere = [
            {
                "type": "input",
                "name": "tag",
                "message": "Entrez un tag pour filtrer la recherche :",
            },
            {
                "type": "input",
                "name": "limit",
                "message": "Combien de résultats voulez-vous afficher ? (par défaut: 10) :",
                "validate": lambda val: val.isdigit() and int(val) > 0,
            },  # validate : returns true si l'input est un entier sous forme de str et s'il
            # est positif l'utilisation du mot clé lambda permet de définir une fonction en
            # une ligne et évite de la définir ailleurs.
        ]

    def make_choice(self):
        while True:
            choix = prompt(self.questions)["Menu recherche"]

            if choix == "Ajouter un critère de recherche":
                reponse_critere = prompt(self.question_critere)
                if Recherche().ajouter_critere(reponse_critere=reponse_critere):
                    print("Critère ajouté:", Recherche().dict_critere)
            elif choix == "Réinitialiser les critères":
                if Recherche().reinitialiser_criteres():
                    print("Critères de recherche réinitialisés.")
            elif choix == "Lancer la recherche":
                Recherche().lancer_recherche()
                if Recherche().etat_recherche == 0:
                    print("Aucun son trouvé avec les critères de recherche.")
                if Recherche().etat_recherche == -1:
                    print("Aucun critère spécifié pour la recherche. Veuillez ajouter un critère.")
            elif choix == "Quitter le menu recherche":
                print("Retour au menu principal.")
                break

    def display_info(self):
        print(Fore.BLUE + " MENU DE RECHERCHE ".center(80, "=") + Style.RESET_ALL)
