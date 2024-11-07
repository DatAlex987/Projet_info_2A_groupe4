"""Ce module implémente la view d'accueil"""

from colorama import Fore, Style
from InquirerPy import prompt
from view.abstractview import AbstractView
from view.menuprincipalview import MenuPrincipalView
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
            {"type": "input", "name": "pseudo", "message": "Veuillez entrer votre pseudo:"},
            {"type": "input", "name": "nom", "message": "Veuillez entrer votre nom:"},
            {"type": "input", "name": "prenom", "message": "Veuillez entrer votre prénom:"},
            {
                "type": "password",
                "name": "mdp",
                "message": "Veuillez entrer votre mot de passe:",
            },  # Avec le type password, l'input est remplacé par des "*"
        ]
        self.questions_creation_compte = [
            {"type": "input", "name": "nom", "message": "Veuillez entrer votre nom:"},
            {"type": "input", "name": "prenom", "message": "Veuillez entrer votre prénom:"},
            {
                "type": "input",
                "name": "date_naissance",
                "message": "Veuillez entrer votre date de naissance au format JJ/MM/AAAA:",
            },
            {"type": "input", "name": "pseudo", "message": "Veuillez choisir votre pseudo:"},
            {
                "type": "password",
                "name": "mdp",
                "message": "Veuillez entrer votre mot de passe:",
            },  # Avec le type password, l'input est remplacé par des "*"
        ]

    def make_choice(self):
        answers = prompt(self.question)
        if answers["Menu principal"] == "Se connecter":
            est_connecte = False
            while not est_connecte:
                identifiants = prompt(self.questions_identifiants)
                try:
                    UserService().authenticate_user(
                        nom=identifiants["nom"],
                        prenom=identifiants["prenom"],
                        pseudo=identifiants["pseudo"],
                        mdp=identifiants["mdp"],
                        schema="ProjetInfo",
                    )
                    est_connecte = True
                    print("Connecté avec succès")
                    next_view = MenuPrincipalView()
                except ValueError:
                    raise ValueError("L'authentification a échoué")

        if answers["Menu principal"] == "Créer un compte":
            info_creation_compte = prompt(self.questions_creation_compte)
            try:
                UserService().creer_compte(
                    nom=info_creation_compte["nom"],
                    prenom=info_creation_compte["prenom"],
                    date_naissance=info_creation_compte["date_naissance"],
                    pseudo=info_creation_compte["pseudo"],
                    mdp=info_creation_compte["mdp"],
                    schema="ProjetInfo",
                )
                print("Création du compte OK. Vous voila connecté")
            except ValueError:
                raise ValueError("Echec de la création du compte")

        if answers["Menu principal"] == "Quitter l'appli":
            next_view = None

        return next_view

    def display_info(self):
        print(Fore.BLUE + " MENU D'ACCUEIL' ".center(80, "=") + Style.RESET_ALL)
