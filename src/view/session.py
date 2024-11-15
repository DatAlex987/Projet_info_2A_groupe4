from datetime import datetime
from business_object.user import User
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
        self.sd_to_param = None  # Permet de stocker les choix de naviguation de l'utilisateur
        self.scene_to_param = None  # Permet de stocker les choix de naviguation de l'utilisateur
        self.son_to_param = None  # Permet de stocker les choix de naviguation de l'utilisateur
        self.son_to_dl = None  # Permet de stocker les choix de naviguation de l'utilisateur
        self.sd_to_play = None  # Permet de stocker les choix de naviguation de l'utilisateur
        self.scene_to_play = None  # Permet de stocker les choix de naviguation de l'utilisateur
        self.son_to_play = None  # Permet de stocker les choix de naviguation de l'utilisateur
        self.users_to_consult = None
        self.sds_to_consult = None
        self.user_to_consult = None
        self.sd_to_consult = None
        self.scene_to_consult = None
        self.son_to_consult = None
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
        # Appels DAO pour supprimer les objets non reliés en BDD.

    def afficher(self):
        if self.utilisateur is None:
            print("Il n'y pas de session active")
        else:
            print(
                f"Nom: {self.utilisateur.nom} \n Prenom: {self.utilisateur.prenom}"
                + f"\n Id: {self.utilisateur.id_user} \n Debut_connexion: {self.debut_connexion}"
            )
