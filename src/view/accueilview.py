"""Ce module implémente la view d'accueil"""

from colorama import Fore, Style
from InquirerPy import prompt
import psycopg2
from view.abstractview import AbstractView
from view.menuprincipalview import MenuPrincipalView
from service.user_service import UserService
from service.session import Session


class AccueilView(AbstractView):
    """Classe représentant la view d'accueil de l'application."""

    def __init__(self):
        super().__init__()
        self.question = [
            {
                "type": "list",
                "name": "Choix connexion",
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
                "message": "Veuillez entrer votre mot de passe (8 caractères dont: 1 maj, 1 chiffre, 1 symbole):",
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
                "message": "Veuillez entrer votre mot de passe(8 caractères dont: 1 maj, 1 chiffre, 1 symbole):",
            },  # Avec le type password, l'input est remplacé par des "*"
        ]

    def make_choice(self):
        answers = prompt(self.question)
        if answers["Choix connexion"] == "Se connecter":
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
                    print(
                        Fore.GREEN
                        + f"Connexion réussie. Content de vous revoir {identifiants['prenom']}."
                        + Style.RESET_ALL
                    )
                    next_view = MenuPrincipalView()
                except ValueError as e:
                    print(Fore.RED + f"Erreur lors de l'authentification : {e}" + Style.RESET_ALL)

        if answers["Choix connexion"] == "Créer un compte":
            connexion_avec_succes = False
            while not connexion_avec_succes:
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
                    print(
                        Fore.GREEN
                        + f"Votre compte a été créé avec succès. Bienvenue {info_creation_compte['prenom']}"
                        + Style.RESET_ALL
                    )
                    connexion_avec_succes = True
                    next_view = MenuPrincipalView()
                except (ValueError, psycopg2.Error) as e:
                    print(Fore.RED + f"Echec lors de la création du compte : {e}" + Style.RESET_ALL)
                    next_view = AccueilView()

        if answers["Choix connexion"] == "Quitter l'appli":
            Session().deconnexion()
            next_view = None

        return next_view

    def display_info(self):
        print(Style.BRIGHT + Fore.BLUE + " MENU D'ACCUEIL ".center(80, "=") + Style.RESET_ALL)
