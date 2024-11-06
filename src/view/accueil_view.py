"""Ce module implémente la view d'accueil"""

from colorama import Fore, Style
from InquirerPy import prompt
from view.abstractview import AbstractView
from service.user_service import UserService


class AccueilView(AbstractView):
    """Classe représentant la view d'accueil de l'application."""

    def __init__(self):
        super().__init__()
        self.question = [
            {
                "type": "list",
                "name": "Menu principal",
                "message": "Que souhaitez-vous faire ?",
                "choices": [
                    "Se connecter",
                    "Créer un compte",
                    "Quitter l'appli",
                ],
            }
        ]
        self.questions_identifiants = [
            {"type": "input", "name": "Nom", "message": "Veuillez entrer votre nom:"},
            {"type": "input", "name": "Prénom", "message": "Veuillez entrer votre prénom:"},
            {
                "type": "password",
                "name": "mdp",
                "message": "Veuillez entrer votre mot de passe:",
            },  # Avec le type password, l'input est remplacé par des "*"
        ]

    def make_choice(self):
        answers = prompt(self.question)
        if answers["Menu principal"] == "Se connecter":
            identifiants = prompt(self.questions_identifiants)
            # Appel de UserService().authenticate_user(pseudo ou nom/prenom)
        if answers["Menu principal"] == "Créer un compte":
            pass
        if answers["Menu principal"] == "Quitter l'appli":
            next_view = None

        return next_view

    def display_info(self):
        print(Fore.BLUE + " MENU D'ACCUEIL' ".center(80, "=") + Style.RESET_ALL)
