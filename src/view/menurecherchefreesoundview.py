"""Ce module implémente la view dédiée à la recherche de sons sur Freesound"""

from colorama import Fore, Style
from InquirerPy import prompt
from view.abstractview import AbstractView

# from view.session import Session
# from service.sd_service import SDService
# from service.scene_service import SceneService
# from service.freesound import Freesound
from service.recherche import Recherche

# from view.accueilview import AccueilView


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
        """self.question_resultats = [
            {
                "type": "list",
                "name": "choix_resultat",
                "message": "Sélectionnez un son ou naviguez dans les pages :",
                "choices": Recherche().formatage_choix_resultats_recherche(),
            }
        ]"""
        self.question_son = [
            {
                "type": "list",
                "name": "question son",
                "message": "Que voulez-vous faire ?",
                "choices": [
                    "Écouter le son",
                    "Sauvegarder dans la scène",
                    "Retour aux résultats de recherche",
                ],
            }
        ]

    # Décorateur qui transforme cette méthode en attribut. Permet de gagner en lisibilité.
    # Ici, indispensable pour update question_resultats à chaque fois que c'est demandé (on run
    # la fonction de formatage qui renvoie de nouveaux choix)
    @property
    def question_resultats(self):
        """Dynamically generate question for search results with updated choices."""
        q = [
            {
                "type": "list",
                "name": "choix_resultat",
                "message": "Sélectionnez un son ou naviguez dans les pages :",
                "choices": Recherche().formatage_choix_resultats_recherche(),
            }
        ]
        return q

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
                resultats = Recherche().lancer_recherche()
                if resultats == []:
                    print("Aucun son n'a été trouvé")
                else:
                    while True:
                        choix_resultat = prompt(self.question_resultats)
                        if choix_resultat["choix_resultat"] == "Page précédente":
                            Recherche().page -= 1
                        elif choix_resultat["choix_resultat"] == "Page suivante":
                            Recherche().page += 1
                        elif choix_resultat["choix_resultat"] == "Retour au menu de recherche":
                            break
                        else:
                            Recherche().afficher_details_son(son=choix_resultat["choix_resultat"])
                            choix_son = prompt(self.question_son)
                            if choix_son["question son"] == "Écouter le son":
                                print("Vers l'écoute du son'")
                            elif choix_son["question son"] == "Sauvegarder dans la scène":
                                print("Vers la sauvegarde")
                            elif choix_son["question son"] == "Retour aux résultats de recherche":
                                pass
            elif choix == "Quitter le menu recherche":
                break
        from view.menuparamscenespecifiqueview import MenuParamSceneSpecifiqueView

        return MenuParamSceneSpecifiqueView()

    def display_info(self):
        print(Fore.BLUE + " MENU DE RECHERCHE ".center(80, "=") + Style.RESET_ALL)
