from datetime import datetime

####
from business_object.user import User
from utils.singleton import Singleton


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
        self.sd_to_param = None  # Permet de stocker les choix de naviguation de l'utilisateur (idem pour les autres)
        self.scene_to_param = None
        self.son_to_param = None
        self.son_to_search = None
        self.son_to_preview = None
        self.sd_to_play = None
        self.scene_to_play = None
        self.son_to_play = None
        # Permet de n'avoir qu'une seule view pour afficher les SDs intéressantes. Cet attribut
        # sera utilisé dans une fonction de formatage de réponses de SDService pour afficher
        # les SDs du user voulues OU les SDs avec un nom similaire à celui recherché (on fait du 2 en 1)
        self.type_recherche_consult = None
        self.users_to_consult = None
        self.sds_to_consult = None
        self.user_to_consult = None
        self.sd_to_consult = None
        self.scene_to_consult = None
        self.son_to_consult = None

    def connexion(self, utilisateur):
        """Enregistement des données en session"""
        self.utilisateur = utilisateur
        self.debut_connexion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def deconnexion(self):
        """Suppression des données de la session"""
        # Imports ici pour éviter les circular imports
        from dao.tag_dao import TagDAO
        from dao.son_dao import SonDAO
        from dao.scene_dao import SceneDAO
        from dao.sd_dao import SDDAO

        SDDAO().delete_sd_if_no_users(schema="ProjetInfo")
        SceneDAO().delete_scene_if_no_sds(schema="ProjetInfo")
        SonDAO().delete_son_if_no_scenes(schema="ProjetInfo")
        TagDAO().delete_tag_if_no_sons(schema="ProjetInfo")

        self.utilisateur = None
        self.debut_connexion = None
