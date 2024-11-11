from utils.log_decorator import log
from business_object.scene import Scene
from business_object.son import Son
from business_object.son_continu import Son_Continu
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_manuel import Son_Manuel
from view.session import Session
import re
import datetime
import random
import string
from dao.scene_dao import SceneDAO
from dao.son_dao import SonDAO
from dao.tag_dao import TagDAO


class SonService:
    """Méthodes de service des sons"""

    def formatage_question_sons_of_scene(self, id_sd: str, id_scene: str):
        """Construit une liste des choix à afficher après sélection d'une Scène

        Params
        -------------
        if_sd : str
            id du SD sélectionné par l'utilisateur
        id_scene : str
            id de la scène sélectionnée par l'utilisateur

        Returns
        -------------
        list
            Liste des choix proposés à l'utilisateur
        """
        sds_user = Session().utilisateur.SD_possedes
        scene_selectionnee = None
        for sd in sds_user:
            if sd.id_sd == id_sd:
                for scene in sd:
                    if scene.id_scene == id_scene:
                        scene_selectionnee = scene
        choix = []
        compteur = 1
        for son_alea in scene_selectionnee.sons_aleatoires:
            mise_en_page_ligne = f"{compteur}. [ALEATOIRE] |{son_alea.nom} | {son_alea.duree} | {son_alea.date_creation}"
            choix.append(mise_en_page_ligne)
            compteur += 1
        choix.append("Ajouter un son via Freesound")
        choix.append("Supprimer la scène")
        choix.append("Retour au menu de choix des sound-decks")
        return choix
