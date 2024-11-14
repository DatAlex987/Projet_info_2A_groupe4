from utils.log_decorator import log
from business_object.scene import Scene
from business_object.son import Son
from business_object.son_continu import Son_Continu
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_manuel import Son_Manuel
from view.session import Session
from service.freesound import Freesound
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
                for scene in sd.scenes:
                    if scene.id_scene == id_scene:
                        scene_selectionnee = scene
        choix = []
        compteur = 1
        for son_alea in scene_selectionnee.sons_aleatoires:
            mise_en_page_ligne = f"{compteur}. {son_alea.id_freesound}| [ALEATOIRE] |{son_alea.nom} | {son_alea.duree}"
            choix.append(mise_en_page_ligne)
            compteur += 1
        for son_cont in scene_selectionnee.sons_continus:
            mise_en_page_ligne = (
                f"{compteur}. {son_cont.id_freesound}| [CONTINU] |{son_cont.nom} | {son_cont.duree}"
            )
            choix.append(mise_en_page_ligne)
            compteur += 1
        for son_manuel in scene_selectionnee.sons_manuels:
            mise_en_page_ligne = f"{compteur}. {son_manuel.id_freesound}| [MANUEL] |{son_manuel.nom} | {son_manuel.duree}"
            choix.append(mise_en_page_ligne)
            compteur += 1
        choix.append("Ajouter un son via Freesound")
        choix.append("Supprimer la scène")
        choix.append("Retour au menu de choix des scènes")
        return choix

    def formatage_question_sons_of_scene_menu_jeu(self, id_sd: str, id_scene: str):
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
                for scene in sd.scenes:
                    if scene.id_scene == id_scene:
                        scene_selectionnee = scene
        choix = []
        compteur = 1
        for son_alea in scene_selectionnee.sons_aleatoires:
            mise_en_page_ligne = (
                f"{compteur}. [ALEATOIRE] |{son_alea.nom}|{son_alea.id_freesound}|' '| 'Etat'"
            )
            choix.append(mise_en_page_ligne)
            compteur += 1
        for son_cont in scene_selectionnee.sons_continus:
            mise_en_page_ligne = (
                f"{compteur}. [CONTINU] |{son_cont.nom}|{son_cont.id_freesound}|' '| 'Etat'"
            )
            choix.append(mise_en_page_ligne)
            compteur += 1
        for son_manuel in scene_selectionnee.sons_manuels:
            mise_en_page_ligne = f"{compteur}. [MANUEL] |{son_manuel.nom}|{son_manuel.id_freesound}|{son_manuel.start_key}| 'Etat'"
            choix.append(mise_en_page_ligne)
            compteur += 1
        choix.append("Retour au menu de choix des scènes")
        return choix

    def ajouter_nouveau_son(self, son_kwargs: dict, schema: str):
        if son_kwargs["type_son"] == "Son aléatoire":
            son_to_add = Son_Aleatoire(
                nom=son_kwargs["name"],
                description=son_kwargs["description"],
                duree=datetime.timedelta(seconds=son_kwargs["duration"]),
                id_freesound=son_kwargs["id"],
                tags=son_kwargs["tags"],
                cooldown_min=int(son_kwargs["param1"]),
                cooldown_max=int(son_kwargs["param2"]),
            )
        if son_kwargs["type_son"] == "Son manuel":
            son_to_add = Son_Manuel(
                nom=son_kwargs["name"],
                description=son_kwargs["description"],
                duree=datetime.timedelta(seconds=son_kwargs["duration"]),
                id_freesound=son_kwargs["id"],
                tags=son_kwargs["tags"],
                start_key=son_kwargs["param1"],
            )
        if son_kwargs["type_son"] == "Son continu":
            son_to_add = Son_Continu(
                nom=son_kwargs["name"],
                description=son_kwargs["description"],
                duree=datetime.timedelta(seconds=son_kwargs["duration"]),
                id_freesound=son_kwargs["id"],
                tags=son_kwargs["tags"],
            )

        try:
            # On commence par ajouter le son
            SonDAO().ajouter_son(son=son_to_add, schema=schema)
            # Puis on le relie à la bonne scène
            SonDAO().ajouter_association_scene_son(
                id_scene=Session().scene_to_param.id_scene, son=son_to_add, schema=schema
            )

            all_tags = TagDAO().consulter_tags
            # On ajoute les tags du son non déjà présents en BDD
            for tag in son_to_add.tags:
                if tag not in all_tags:
                    TagDAO().ajouter_tag(tag=tag, schema=schema)
            # Puis pour chaque tag du son, on le lie au son
            for tag in son_to_add.tags:
                TagDAO().ajouter_association_son_tag(
                    id_freesound=son_to_add.id_freesound, tag="X", schema=schema
                )

            # Enfin, on le télécharge:
            Freesound().telecharger_son(id_son=son_to_add.id_freesound)
        except ValueError as e:
            raise ValueError(f"{e}")

    def instancier_son_par_id_type(self, id_freesound: str, type_son: str, schema: str):
        """Instancie un son (et tous ses tags) à partir de son id et de son type

        Params
        -------------
        id_freesound : str
            id du son sélectionné par l'utilisateur
        type_son : str
            Type du son à instancier
        schema : str
            Schéma sur lequel faire les requêtes
        Returns
        -------------
        Son_Aleatoire or Son_Manuel or Son_Continu
            Instance du son demandé
        """
        if type_son == "ALEATOIRE":
            # On commence par recherche le son en BDD
            son_kwargs = SonDAO().rechercher_par_id_son(id_freesound=id_freesound, schema=schema)
            # Puis on recherche ses paramètres dans la table d'association scene_son
            additional_son_kwargs = {}
            sons_of_scene = SonDAO().rechercher_sons_par_scene(
                id_scene=Session().scene_to_param.id_scene, schema=schema
            )
            for son in sons_of_scene["sons_aleatoires"]:
                if son["id_freesound"] == id_freesound:
                    additional_son_kwargs["param1"] = son["param1"]
                    additional_son_kwargs["param2"] = son["param2"]
            # Enfin, on peut l'instancier avec tous nos éléments
            instance_son = Son_Aleatoire(
                nom=son_kwargs["nom"],
                description=son_kwargs["description"],
                duree=datetime.timedelta(
                    hours=son_kwargs["duree"].hour,
                    minutes=son_kwargs["duree"].minute,
                    seconds=son_kwargs["duree"].second,
                ),
                id_freesound=son_kwargs["id_freesound"],
                tags=SonDAO().get_tags_of_son(id_freesound=id_freesound, schema=schema),
                cooldown_min=additional_son_kwargs["param1"],
                cooldown_max=additional_son_kwargs["param2"],
            )
            return instance_son
        if type_son == "CONTINU":
            # On commence par recherche le son en BDD
            son_kwargs = SonDAO().rechercher_par_id_son(id_freesound=id_freesound, schema=schema)

            # Enfin, on peut l'instancier avec tous nos éléments
            instance_son = Son_Continu(
                nom=son_kwargs["nom"],
                description=son_kwargs["description"],
                duree=son_kwargs["duree"],
                id_freesound=son_kwargs["id_freesound"],
                tags=SonDAO().get_tags_of_son(id_freesound=id_freesound, schema=schema),
            )
            return instance_son
        if type_son == "MANUEL":
            # On commence par recherche le son en BDD
            son_kwargs = SonDAO().rechercher_par_id_son(id_freesound=id_freesound, schema=schema)
            # Puis on recherche ses paramètres dans la table d'association scene_son
            additional_son_kwargs = {}
            sons_of_scene = SonDAO().rechercher_sons_par_scene(
                id_scene=Session().scene_to_param.id_scene, schema=schema
            )
            for son in sons_of_scene["sons_manuels"]:
                if son["id_freesound"] == id_freesound:
                    additional_son_kwargs["param1"] = son["param1"]
            # Enfin, on peut l'instancier avec tous nos éléments
            instance_son = Son_Manuel(
                nom=son_kwargs["nom"],
                description=son_kwargs["description"],
                duree=son_kwargs["duree"],
                id_freesound=son_kwargs["id_freesound"],
                tags=SonDAO().get_tags_of_son(id_freesound=id_freesound, schema=schema),
                start_key=additional_son_kwargs["param1"],
            )
            return instance_son

    def multi_modifications_son(self, son, modif: dict):
        pass

    def modifier_nom_son(self, son, new_nom: str, schema: str):
        son.modifier_nom(new_nom=new_nom)
        SonDAO().modifier_son(son=son, schema=schema)

    def modifier_desc_son(self, son, new_desc: str, schema: str):
        son.modifier_description(new_desc=new_desc)
        SonDAO().modifier_son(son=son, schema=schema)

    def modifier_cdmin_son(self, son_alea: Son_Aleatoire, new_cdmin: int, schema: str):
        son_alea.modifier_cooldown_min(new_cooldown_min=new_cdmin)
        SonDAO().modifier_param_son(son_alea, schema=schema)

    def modifier_cdmax_son(self, son_alea: Son_Aleatoire, new_cdmax: int, schema: str):
        son_alea.modifier_cooldown_max(new_cooldown_min=new_cdmax)
        SonDAO().modifier_param_son(son_alea, schema=schema)

    def modifier_start_key_son(self, son_manuel: Son_Manuel, new_start_key: str, schema: str):
        son_manuel.modifier_start_key(new_start_key=new_start_key)
        SonDAO().modifier_param_son(son_manuel, schema=schema)
