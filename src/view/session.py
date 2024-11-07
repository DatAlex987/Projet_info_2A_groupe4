from datetime import datetime
from src.business_object.user import User
from utils.singleton import Singleton
import pygame


class Session(metaclass=Singleton):
    """Stocke les données liées à une session.
    Cela permet par exemple de connaitre le joueur connecté à tout moment
    depuis n'importe quelle classe.
    Sans cela, il faudrait transmettre ce joueur entre les différentes vues.
    """

    def __init__(self):
        """Création de la session"""
        self.utilisateur: User = None
        self.debut_connexion = None
        self.mixer = pygame.mixer.init()

    def connexion(self, utilisateur):
        """Enregistement des données en session"""
        self.utilisateur = utilisateur
        self.debut_connexion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def deconnexion(self):
        """Suppression des données de la session"""
        self.mixer = pygame.mixer.quit
        self.utilisateur = None
        self.debut_connexion = None

    def afficher(self):
        if self.utilisateur is None:
            print("Il n'y pas de session active")
        else:
            print(
                f"Nom: {self.utilisateur.nom} \n Prenom: {self.utilisateur.prenom}"
                + f"\n Id: {self.utilisateur.id_user} \n Debut_connexion: {self.debut_connexion}"
            )
