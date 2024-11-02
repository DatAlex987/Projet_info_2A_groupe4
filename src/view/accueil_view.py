"""Ce module implémente la view d'accueil"""

import pandas as pd
from colorama import Fore, Style
from InquirerPy import prompt
from project.view.abstract_view import AbstractView
from project.view.client_view import ClientView
from project.client import Client


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
                    "Je suis un agent immobilier",
                    "Je suis un client",
                    "Quitter l'appli",
                ],
            }
        ]
        self.questions_identification = [
            {"type": "confirm", "name": "question compte", "message": "Avez-vous déjà un compte ?"},
            {"type": "input", "name": "question prenom", "message": "Quel est votre prénom ?"},
            {"type": "input", "name": "question nom", "message": "Quel est votre nom ?"},
            {"type": "input", "name": "question age", "message": "Quel est votre âge ?"},
        ]
        self.questions_menu = [
            {
                "type": "list",
                "name": "Menu principal",
                "message": "Que souhaitez-vous faire ?",
                "choices": [
                    "Faire estimer un bien",
                    "Poster une annonce",
                    "Consulter les annonces",
                    "Modifier une de mes annonces",
                    "Supprimer une de mes annonces",
                    "Me déconnecter",
                    "Quitter l'application",
                ],
            }
        ]

    def make_choice(self, user_info: str):
        answers = prompt(self.questions)
        if answers["Menu principal"] == "Je suis un agent immobilier":
            from project.view.agentimmo_view import AgentImmoView

            next_view = AgentImmoView()
            user_info = ""
        elif answers["Menu principal"] == "Je suis un client":
            answers_id = prompt(self.questions_identification)
            # Si le client a déjà un compte :
            if answers_id["question compte"]:
                bdd_clients = pd.read_csv("resources/bdd_client.csv")
                # La réponse est stockée en str, on la passe en int:
                answers_id["question age"] = int(answers_id["question age"])
                resultats_potentiels = bdd_clients.query(
                    'nom == @answers_id["question nom"] and prenom == @answers_id["question prenom"] and age == @answers_id["question age"]',
                    engine="python",
                )
                # Dans le cas où un unique client correspond :
                if len(resultats_potentiels) == 1:
                    identifiant = resultats_potentiels["id_client"].iloc[0]
                    user = Client(
                        answers_id["question prenom"],
                        answers_id["question nom"],
                        int(answers_id["question age"]),
                        str(identifiant),
                    )
                    print(
                        Fore.GREEN
                        + f"Authentification réussie! Bienvenue {user.prenom} {user.nom} (id:{user.id_client})"
                        + Style.RESET_ALL
                    )
                # Dans le cas où plusieurs clients correspondent,
                # il rentre son id :
                elif len(resultats_potentiels) > 1:
                    print(
                        "Plusieurs comptes existent avec ces mêmes "
                        "renseignements. Veuillez renseigner votre "
                        "identifiant unique:"
                    )
                    identifiant = input("Entrez votre identifiant " "(format : XXXX):")
                    if len(bdd_clients.query("id_client == @identifiant")) == 1:
                        user = Client(
                            answers_id["question prenom"],
                            answers_id["question nom"],
                            int(answers_id["question age"]),
                            str(identifiant),
                        )
                        print(
                            Fore.GREEN
                            + f"Authentification réussie! Bienvenue {user.prenom} {user.nom} (id:{user.id_client})"
                            + Style.RESET_ALL
                        )
                    else:
                        print(
                            Fore.RED
                            + "Aucun client trouvé avec ces informations."
                            + Style.RESET_ALL
                        )
                        return [AccueilView(), ""]
                # Dans le cas où aucun client ne correspond :
                else:
                    print(Fore.RED + "Aucun client trouvé avec ces informations." + Style.RESET_ALL)
                    return [AccueilView(), ""]
            # Si le client n'a pas encore de compte :
            if answers_id["question compte"] is False:
                # On lui créé un nouveau compte
                user = Client(
                    answers_id["question prenom"],
                    answers_id["question nom"],
                    int(answers_id["question age"]),
                    "temp_id",
                )
                user.creer_compte()
            return [ClientView(), user]
        elif answers["Menu principal"] == "Quitter l'appli":
            next_view = None
        else:
            next_view = AccueilView()

        return [next_view, ""]

    def display_info(self):
        print(Fore.BLUE + " MENU D'AUTHENTIFICATION ".center(80, "=") + Style.RESET_ALL)
