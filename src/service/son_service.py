import re
import datetime
import random
import string
import pygame
import time

####
from dao.scene_dao import SceneDAO
from dao.son_dao import SonDAO
from dao.tag_dao import TagDAO

####
from business_object.scene import Scene
from business_object.son import Son
from business_object.son_continu import Son_Continu
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_manuel import Son_Manuel

####
from service.session import Session
from service.freesound import Freesound
from service.sd_service import SDService

####
from rich.console import Console
from rich.table import Table
from rich.style import Style


class SonService:
    """Méthodes de service des sons"""

    def __init__(self):
        self.sounds = []

    @staticmethod  # Ne nécessite pas d'instance de SonService pour exister
    def id_son_generator():
        """Génère un identifiant pour un son.

        Identifiant de la forme XYZRSTUV où X,Y,Z,R,S,T,U,V sont des caractères alphanumériques

        Returns:
        -------------------------
        str
            Identifiant (supposé unique) généré pour un son.
        """
        all_sons = SonDAO().consulter_sons(schema="ProjetInfo")
        all_ids = [son["id_son"] for son in all_sons]
        generation = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        unique_id = f"{generation}"
        while unique_id in all_ids:  # On vérifie que l'id n'existe pas déjà
            generation = "".join(random.choices(string.ascii_letters + string.digits, k=8))
            unique_id = f"{generation}"
        return unique_id

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
            mise_en_page_ligne = (
                f"{compteur}. {son_alea.id_son}| [ALEATOIRE] |{son_alea.nom} | {son_alea.duree}"
            )
            choix.append(mise_en_page_ligne)
            compteur += 1
        for son_cont in scene_selectionnee.sons_continus:
            mise_en_page_ligne = (
                f"{compteur}. {son_cont.id_son}| [CONTINU] |{son_cont.nom} | {son_cont.duree}"
            )
            choix.append(mise_en_page_ligne)
            compteur += 1
        for son_manuel in scene_selectionnee.sons_manuels:
            mise_en_page_ligne = (
                f"{compteur}. {son_manuel.id_son}| [MANUEL] |{son_manuel.nom} | {son_manuel.duree}"
            )
            choix.append(mise_en_page_ligne)
            compteur += 1
        choix.append("Ajouter un son via Freesound")
        choix.append("Supprimer la scène")
        choix.append("Modifier la scène")
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
            mise_en_page_ligne = f"{compteur}. [ALEATOIRE] |{son_alea.nom}|{son_alea.id_freesound}|{son_alea.id_son}|' '| 'Etat'"
            choix.append(mise_en_page_ligne)
            compteur += 1
        for son_cont in scene_selectionnee.sons_continus:
            mise_en_page_ligne = f"{compteur}. [CONTINU] |{son_cont.nom}|{son_cont.id_freesound}|{son_cont.id_son}|' '| 'Etat'"
            choix.append(mise_en_page_ligne)
            compteur += 1
        for son_manuel in scene_selectionnee.sons_manuels:
            mise_en_page_ligne = f"{compteur}. [MANUEL] |{son_manuel.nom}|{son_manuel.id_freesound}|{son_manuel.id_son}|{son_manuel.start_key}| 'Etat'"
            choix.append(mise_en_page_ligne)
            compteur += 1
        choix.append("Retour au menu de choix des scènes")
        return choix

    def formatage_question_sons_of_scene_menu_consult(self, id_sd: str, id_scene: str):
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
        sds_consult = Session().sds_to_consult
        scene_selectionnee = None
        for sd in sds_consult:
            if sd.id_sd == id_sd:
                for scene in sd.scenes:
                    if scene.id_scene == id_scene:
                        scene_selectionnee = scene
        choix = []
        compteur = 1
        for son_alea in scene_selectionnee.sons_aleatoires:
            mise_en_page_ligne = f"{compteur}. [ALEATOIRE] |{son_alea.nom}|{son_alea.id_freesound}|{son_alea.id_son}|' '| 'Etat'"
            choix.append(mise_en_page_ligne)
            compteur += 1
        for son_cont in scene_selectionnee.sons_continus:
            mise_en_page_ligne = f"{compteur}. [CONTINU] |{son_cont.nom}|{son_cont.id_freesound}|{son_cont.id_son}|' '| 'Etat'"
            choix.append(mise_en_page_ligne)
            compteur += 1
        for son_manuel in scene_selectionnee.sons_manuels:
            mise_en_page_ligne = f"{compteur}. [MANUEL] |{son_manuel.nom}|{son_manuel.id_freesound}|{son_manuel.id_son}|{son_manuel.start_key}| 'Etat'"
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
                id_freesound=str(son_kwargs["id"]),
                id_son=SonService.id_son_generator(),
                tags=son_kwargs["tags"],
                cooldown_min=int(son_kwargs["param1"]),
                cooldown_max=int(son_kwargs["param2"]),
            )
        if son_kwargs["type_son"] == "Son manuel":
            son_to_add = Son_Manuel(
                nom=son_kwargs["name"],
                description=son_kwargs["description"],
                duree=datetime.timedelta(seconds=son_kwargs["duration"]),
                id_freesound=str(son_kwargs["id"]),
                id_son=SonService.id_son_generator(),
                tags=son_kwargs["tags"],
                start_key=son_kwargs["param1"],
            )
        if son_kwargs["type_son"] == "Son continu":
            son_to_add = Son_Continu(
                nom=son_kwargs["name"],
                description=son_kwargs["description"],
                duree=datetime.timedelta(seconds=son_kwargs["duration"]),
                id_freesound=str(son_kwargs["id"]),
                id_son=SonService.id_son_generator(),
                tags=son_kwargs["tags"],
            )

        try:
            # On commence par ajouter le son
            SonDAO().ajouter_son(son=son_to_add, schema=schema)
            # Puis on le relie à la bonne scène
            SonDAO().ajouter_association_scene_son(
                id_scene=Session().scene_to_param.id_scene, son=son_to_add, schema=schema
            )

            all_tags = TagDAO().consulter_tags(schema=schema)
            # On ajoute les tags du son non déjà présents en BDD
            for tag in son_to_add.tags:
                if tag not in all_tags:
                    TagDAO().ajouter_tag(tag=tag, schema=schema)
            # Puis pour chaque tag du son, on le lie au son
            for tag in son_to_add.tags:
                TagDAO().ajouter_association_son_tag(
                    id_son=son_to_add.id_son, tag=tag, schema=schema
                )

            # Enfin, on le télécharge avec son id_freesound:
            Freesound().telecharger_son(id_freesound=son_to_add.id_freesound)
        except ValueError as e:
            raise ValueError(f"{e}")

    def instancier_son_par_id_type(self, id_son: str, type_son: str, schema: str):
        """Instancie un son (et tous ses tags) à partir de son id et de son type

        Params
        -------------
        id_son : str
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
            son_kwargs = SonDAO().rechercher_par_id_son(id_son=id_son, schema=schema)
            # Puis on recherche ses paramètres dans la table d'association scene_son
            additional_son_kwargs = {}
            sons_of_scene = SonDAO().rechercher_sons_par_scene(
                id_scene=Session().scene_to_param.id_scene, schema=schema
            )
            for son in sons_of_scene["sons_aleatoires"]:
                if son["id_son"] == id_son:
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
                id_son=son_kwargs["id_son"],
                tags=SonDAO().get_tags_of_son(id_son=id_son, schema=schema),
                cooldown_min=additional_son_kwargs["param1"],
                cooldown_max=additional_son_kwargs["param2"],
            )
            return instance_son
        if type_son == "CONTINU":
            # On commence par recherche le son en BDD
            son_kwargs = SonDAO().rechercher_par_id_son(id_son=id_son, schema=schema)

            # Enfin, on peut l'instancier avec tous nos éléments
            instance_son = Son_Continu(
                nom=son_kwargs["nom"],
                description=son_kwargs["description"],
                duree=datetime.timedelta(
                    hours=son_kwargs["duree"].hour,
                    minutes=son_kwargs["duree"].minute,
                    seconds=son_kwargs["duree"].second,
                ),
                id_freesound=son_kwargs["id_freesound"],
                id_son=son_kwargs["id_son"],
                tags=SonDAO().get_tags_of_son(id_son=id_son, schema=schema),
            )
            return instance_son
        if type_son == "MANUEL":
            # On commence par recherche le son en BDD
            son_kwargs = SonDAO().rechercher_par_id_son(id_son=id_son, schema=schema)
            # Puis on recherche ses paramètres dans la table d'association scene_son
            additional_son_kwargs = {}
            sons_of_scene = SonDAO().rechercher_sons_par_scene(
                id_scene=Session().scene_to_param.id_scene, schema=schema
            )
            for son in sons_of_scene["sons_manuels"]:
                if son["id_son"] == id_son:
                    additional_son_kwargs["param1"] = son["param1"]
            # Enfin, on peut l'instancier avec tous nos éléments
            instance_son = Son_Manuel(
                nom=son_kwargs["nom"],
                description=son_kwargs["description"],
                duree=datetime.timedelta(
                    hours=son_kwargs["duree"].hour,
                    minutes=son_kwargs["duree"].minute,
                    seconds=son_kwargs["duree"].second,
                ),
                id_freesound=son_kwargs["id_freesound"],
                id_son=son_kwargs["id_son"],
                tags=SonDAO().get_tags_of_son(id_son=id_son, schema=schema),
                start_key=additional_son_kwargs["param1"],
            )
            return instance_son

    def modifier_nom_son(self, son, new_nom: str, schema: str):
        SDService().input_checking_injection(input_str=new_nom)
        # On update la session
        son.modifier_nom(new_nom=new_nom)
        # On update le user en session
        for sd in Session().utilisateur.SD_possedes:
            for scene in sd.scenes:
                if isinstance(son, Son_Aleatoire):
                    for son_alea in scene.sons_aleatoires:
                        if son_alea.id_son == son.id_son:
                            son_alea.modifier_nom(new_nom=new_nom)
                if isinstance(son, Son_Continu):
                    for son_continu in scene.sons_continus:
                        if son_continu.id_son == son.id_son:
                            son_continu.modifier_nom(new_nom=new_nom)
                if isinstance(son, Son_Manuel):
                    for son_manuel in scene.sons_manuels:
                        if son_manuel.id_son == son.id_son:
                            son_manuel.modifier_nom(new_nom=new_nom)
        # On update la BDD
        SonDAO().modifier_son(son=son, schema=schema)

    def modifier_desc_son(self, son, new_desc: str, schema: str):
        SDService().input_checking_injection(input_str=new_desc)
        # On update la session
        son.modifier_description(new_desc=new_desc)
        # On update le user en session
        for sd in Session().utilisateur.SD_possedes:
            for scene in sd.scenes:
                if isinstance(son, Son_Aleatoire):
                    for son_alea in scene.sons_aleatoires:
                        if son_alea.id_son == son.id_son:
                            son_alea.modifier_description(new_description=new_desc)
                if isinstance(son, Son_Continu):
                    for son_continu in scene.sons_continus:
                        if son_continu.id_son == son.id_son:
                            son_continu.modifier_description(new_description=new_desc)
                if isinstance(son, Son_Manuel):
                    for son_manuel in scene.sons_manuels:
                        if son_manuel.id_son == son.id_son:
                            son_manuel.modifier_description(new_description=new_desc)
        # On update la BDD
        SonDAO().modifier_son(son=son, schema=schema)

    def modifier_cdmin_son(self, son_alea: Son_Aleatoire, new_cdmin: int, schema: str):
        son_alea.modifier_cooldown_min(new_cooldown_min=int(new_cdmin))
        for sd in Session().utilisateur.SD_possedes:
            for scene in sd.scenes:
                for son in scene.sons_aleatoires:
                    if son.id_son == son_alea.id_son:
                        son.modifier_cooldown_min(new_cooldown_min=int(new_cdmin))

        SonDAO().modifier_param_son(son_alea, schema=schema)

    def modifier_cdmax_son(self, son_alea: Son_Aleatoire, new_cdmax: int, schema: str):
        son_alea.modifier_cooldown_max(new_cooldown_max=int(new_cdmax))
        for sd in Session().utilisateur.SD_possedes:
            for scene in sd.scenes:
                for son in scene.sons_aleatoires:
                    if son.id_son == son_alea.id_son:
                        son.modifier_cooldown_max(new_cooldown_max=int(new_cdmax))
        SonDAO().modifier_param_son(son_alea, schema=schema)

    def modifier_start_key_son(self, son_manuel: Son_Manuel, new_start_key: str, schema: str):
        SDService().input_checking_injection(input_str=new_start_key)
        son_manuel.modifier_start_key(new_start_key=new_start_key)
        for sd in Session().utilisateur.SD_possedes:
            for scene in sd.scenes:
                for son in scene.sons_manuels:
                    if son.id_son == son_manuel.id_son:
                        son.modifier_start_key(new_start_key=new_start_key)
        SonDAO().modifier_param_son(son_manuel, schema=schema)

    def afficher_details_son_continu(self, son_continu):
        """Affiche les détails d'un son continu."""
        console = Console()
        table = Table(
            show_header=True,
            header_style=Style(color="chartreuse1", bold=True),
            title="--------------- Détails du Son Continu ---------------",
            style="white",
        )
        table.add_column("Champ", style=Style(color="honeydew2"), width=20)
        table.add_column("Détails", style=Style(color="honeydew2"))

        table.add_row("ID du son", str(son_continu.id_son))
        table.add_row("ID Freesound", str(son_continu.id_freesound))
        table.add_row("Nom", son_continu.nom)
        table.add_row("Tags", ", ".join(son_continu.tags[:5]))
        table.add_row(
            "Durée",
            f"{int(son_continu.duree.total_seconds() // 60)} min {int(son_continu.duree.total_seconds() % 60)} sec",
        )

        console.print(table)

    def afficher_details_son_manuel(self, son_manuel):
        """Affiche les détails d'un son manuel."""
        console = Console()
        table = Table(
            show_header=True,
            header_style=Style(color="chartreuse1", bold=True),
            title="--------------- Détails du Son Manuel ---------------",
            style="white",
        )
        table.add_column("Champ", style=Style(color="honeydew2"), width=20)
        table.add_column("Détails", style=Style(color="honeydew2"))

        table.add_row("ID du son", str(son_manuel.id_son))
        table.add_row("ID Freesound", str(son_manuel.id_freesound))
        table.add_row("Nom", son_manuel.nom)
        table.add_row("Tags", ", ".join(son_manuel.tags[:5]))
        table.add_row(
            "Durée",
            f"{int(son_manuel.duree.total_seconds() // 60)} min {int(son_manuel.duree.total_seconds() % 60)} sec",
        )
        table.add_row("Touche de démarrage", son_manuel.start_key)

        console.print(table)

    def afficher_details_son_aleatoire(self, son_aleatoire):
        """Affiche les détails d'un son aléatoire."""
        console = Console()
        table = Table(
            show_header=True,
            header_style=Style(color="chartreuse1", bold=True),
            title="--------------- Détails du Son Aléatoire ---------------",
            style="white",
        )
        table.add_column("Champ", style=Style(color="honeydew2"), width=20)
        table.add_column("Détails", style=Style(color="honeydew2"))

        table.add_row("ID du son", str(son_aleatoire.id_son))
        table.add_row("ID Freesound", str(son_aleatoire.id_freesound))
        table.add_row("Nom", son_aleatoire.nom)
        table.add_row("Tags", ", ".join(son_aleatoire.tags[:5]))
        table.add_row(
            "Durée",
            f"{int(son_aleatoire.duree.total_seconds() // 60)} min {int(son_aleatoire.duree.total_seconds() % 60)} sec",
        )
        table.add_row("Cooldown Min", f"{son_aleatoire.cooldown_min} sec")
        table.add_row("Cooldown Max", f"{son_aleatoire.cooldown_max} sec")

        console.print(table)

    def previsualiser_son(self, son: Son):
        son_kwargs = Session().son_to_search
        son = Son(
            nom=son_kwargs["name"],
            description=son_kwargs["description"],
            duree=datetime.timedelta(seconds=son_kwargs["duration"]),
            id_son="",  # Pas d'id_son car pas encore dans la BDD
            id_freesound=str(son_kwargs["id"]),
            tags=son_kwargs["tags"],
        )

        Freesound().telecharger_son(id_freesound=son.id_freesound)
        son.jouer_son_preview()
        print("Ecoute en cours... (10secondes)")
        time.sleep(12)
        pygame.mixer.music.stop()  # Pour arrêter le MP3 (sinon impossible de le supprimer)
        Freesound().supprimer_son(id_freesound=son.id_freesound)
