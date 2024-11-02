"""Ce module implémente la view d'accueil"""

from colorama import Fore, Style
from InquirerPy import prompt
from view.abstract_view import AbstractView


class AccueilView(AbstractView):
    """Classe représentant la view d'accueil de l'application."""

    def __init__(self):
        super().__init__()
        self.questions = [
            {
                "type": "list",
                "name": "Menu principal",
                "message": "Merci de vous identifier.",
                "choices": [
                    "Se connecter",
                    "Créer un compte",
                    "Quitter l'appli",
                ],
            }
        ]
        self.questions_identification = [
            {"type": "input", "name": "question pseudo", "message": "Quel est votre pseudo ?"},
            {"type": "input", "name": "question mdp", "message": "Quel est votre mot de passe ?"},
        ]

    def make_choice(self, user_info: str):
        answers = prompt(self.questions)
        next_view = None
        return [next_view, ""]

    def display_info(self):
        print(Fore.BLUE + " MENU DE CONNEXION ".center(80, "=") + Style.RESET_ALL)
