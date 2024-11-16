from business_object.scene import Scene
from business_object.son import Son
from business_object.son_continu import Son_Continu
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_manuel import Son_Manuel
from service.session import Session
import re
import datetime
import random
import string
from dao.scene_dao import SceneDAO
from dao.son_dao import SonDAO
from dao.tag_dao import TagDAO


class SceneService:
    """Méthodes de service des scènes"""

    def input_checking_injection(self, nom: str, description: str):
        """Vérifier les inputs de l'utilisateur pour empêcher les injections SQL

        Params
        -------------
        nom : str
            nom entré par l'utilisateur
        description : str
            description entrée par l'utilisateur
        """
        # Check inputs pour injection:
        # Définition de pattern regex pour qualifier les caractères acceptés pour chaque input
        pattern = r"^[a-zA-Zà-öø-ÿÀ-ÖØ-ß\s0-9\s,.\-:!@#%^&*()_+=|?/\[\]{}']*$"  # Autorise lettres, et autres caractères
        # On vérifie que les inputs sont conformes aux patternes regex.
        if not re.match(pattern, nom):
            raise ValueError("Le nom de la scène contient des caractères invalides.")
        if not re.match(pattern, description):
            raise ValueError("La description de la scène contient des caractères invalides.")

    @staticmethod  # Ne nécessite pas d'instance de SceneService pour exister
    def id_scene_generator():
        """Génère un identifiant pour une scène.

        Identifiant de la forme XYZRSTU où X,Y,Z,R,S,T,U sont des caractères alphanumériques

        Returns:
        -------------------------
        str
            Identifiant (supposé unique) généré pour une Scène.
        """
        generation = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        unique_id = f"{generation}"
        return unique_id

    def formatage_question_scenes_of_sd(self, id_sd: str):
        """Construit une liste des choix à afficher après sélection d'une SD

        Params
        -------------
        id_sd : str
            id du SD sélectionné par l'utilisateur

        Returns
        -------------
        list
            Liste des choix proposés à l'utilisateur
        """
        sds_user = Session().utilisateur.SD_possedes
        sd_selectionne = None
        for sd in sds_user:
            if sd.id_sd == id_sd:
                sd_selectionne = sd
        choix = []
        compteur = 1
        for scene in sd_selectionne.scenes:
            mise_en_page_ligne = (
                f"{compteur}. {scene.id_scene} | {scene.nom} | {scene.date_creation}"
            )
            choix.append(mise_en_page_ligne)
            compteur += 1
        choix.append("Ajouter une scène")
        choix.append("Supprimer la sound-deck")
        choix.append("Modifier la sound-deck")
        choix.append("Retour au menu de choix des sound-decks")
        return choix

    def creer_scene(self, nom: str, description: str, schema: str):
        """Instancie une scène avec les inputs de l'utilisateur et l'ajoute dans la BDD

        Param
        ------------
        nom : str
            nom donné à la scène par l'utilisateur
        description : str
            description donnée à la scène par l'utilisateur
        schema : str
            schema sur lequel opérer l'ajout de la scène

        Returns
        ------------
        bool
            True si la création à eu lieu sans soulever d'erreur, rien sinon
        """
        SceneService().input_checking_injection(nom=nom, description=description)
        try:
            new_scene = Scene(
                nom=nom,
                description=description,
                id_scene=SceneService.id_scene_generator(),
                sons_aleatoires=[],
                sons_continus=[],
                sons_manuels=[],
                date_creation=datetime.datetime.today().date(),
            )
            SceneDAO().ajouter_scene(scene=new_scene, schema=schema)
            SceneDAO().ajouter_association_sd_scene(
                id_sd=Session().sd_to_param.id_sd, id_scene=new_scene.id_scene, schema=schema
            )
            Session().utilisateur.ajouter_scene_a_sd(
                id_sd=Session().sd_to_param.id_sd, scene=new_scene
            )
            return True
        except ValueError as e:
            raise ValueError(f"{e}")

    def formatage_question_scenes_of_sd_menu_jeu(self, id_sd: str):
        sds_user = Session().utilisateur.SD_possedes
        sd_selectionne = None
        for sd in sds_user:
            if sd.id_sd == id_sd:
                sd_selectionne = sd
        choix = []
        compteur = 1
        for scene in sd_selectionne.scenes:
            mise_en_page_ligne = (
                f"{compteur}. {scene.id_scene} | {scene.nom} | {scene.date_creation}"
            )
            choix.append(mise_en_page_ligne)
            compteur += 1
        choix.append("Retour au menu de choix des sound-decks")
        return choix

    def instancier_scene_par_id(self, id_scene: str, schema: str):
        """Instancie une Scène (et tous les sons qui la composent) à partir de son id

        Params
        -------------
        id_scene : str
            id de la scène sélectionnée par l'utilisateur
        schema : str
            Schéma sur lequel faire les requêtes
        Returns
        -------------
        Scene
            Instance de la scène demandée
        """
        scene_kwargs = SceneDAO().rechercher_par_id_scene(id_scene=id_scene, schema=schema)
        Sons_Alea_scene = []
        Sons_Cont_scene = []
        Sons_Manu_scene = []
        for son_alea_kwargs in scene_kwargs["sons_aleatoires"]:
            Sons_Alea_scene.append(
                Son_Aleatoire(
                    nom=son_alea_kwargs["nom"],
                    description=son_alea_kwargs["description"],
                    duree=son_alea_kwargs["duree"],
                    id_freesound=son_alea_kwargs["id_freesound"],
                    tags=son_alea_kwargs["tags"],
                    cooldown_min=son_alea_kwargs["param1"],
                    cooldown_max=son_alea_kwargs["param2"],
                )
            )
        for son_cont_kwargs in scene_kwargs["sons_continus"]:
            Sons_Cont_scene.append(
                Son_Continu(
                    nom=son_cont_kwargs["nom"],
                    description=son_cont_kwargs["description"],
                    duree=son_cont_kwargs["duree"],
                    id_freesound=son_cont_kwargs["id_freesound"],
                    tags=son_cont_kwargs["tags"],
                )
            )
        for son_manu_kwargs in scene_kwargs["sons_manuels"]:
            Sons_Manu_scene.append(
                Son_Manuel(
                    nom=son_manu_kwargs["nom"],
                    description=son_manu_kwargs["description"],
                    duree=son_manu_kwargs["duree"],
                    id_freesound=son_manu_kwargs["id_freesound"],
                    tags=son_manu_kwargs["tags"],
                    start_key=son_manu_kwargs["param1"],
                )
            )
        scene_to_return = Scene(
            nom=scene_kwargs["nom"],
            description=scene_kwargs["description"],
            id_scene=scene_kwargs["id_scene"],
            sons_aleatoires=Sons_Alea_scene,
            sons_manuels=Sons_Manu_scene,
            sons_continus=Sons_Cont_scene,
            date_creation=scene_kwargs["date_creation"],
        )
        return scene_to_return

    def supprimer_scene(
        self, scene: Scene, schema: str
    ):  # On a besoin de l'objet en entier pour supprimer en "cascade"
        # La suppression d'une Scène supprime l'objet + toutes les associations dans les tables +
        # les associations en cascade. Mais pas les objets en cascade (car ils peuvent tjrs
        # exister dans d'autres Scène)
        """Supprime une Scène dans la BDD ainsi que toutes les associations qui en découlent

        Params
        -------------
        scene : Scene
            Scène à supprimer
        schema : str
            Schema sur lequel opérer la suppression

        Returns
        -------------
        bool
            True si la suppression n'a pas soulevé d'erreur, rien sinon
        """
        try:
            SceneDAO().supprimer_scene(id_scene=scene.id_scene, schema=schema)
            SceneDAO().supprimer_toutes_associations_scene(id_scene=scene.id_scene, schema=schema)
            for son in scene.sons_aleatoires:
                SonDAO().supprimer_toutes_associations_son(
                    id_freesound=son.id_freesound, type_son="aleatoire", schema=schema
                )
                for tag in son.tags:
                    TagDAO().supprimer_association_son_tag(
                        id_freesound=son.id_freesound, tag=tag, schema=schema
                    )
            for son in scene.sons_continus:
                SonDAO().supprimer_toutes_associations_son(
                    id_freesound=son.id_freesound, type_son="continu", schema=schema
                )
                for tag in son.tags:
                    TagDAO().supprimer_association_son_tag(
                        id_freesound=son.id_freesound, tag=tag, schema=schema
                    )
            for son in scene.sons_manuels:
                SonDAO().supprimer_toutes_associations_son(
                    id_freesound=son.id_freesound, type_son="manuel", schema=schema
                )
                for tag in son.tags:
                    TagDAO().supprimer_association_son_tag(
                        id_freesound=son.id_freesound, tag=tag, schema=schema
                    )
            # On termine par actualiser la session
            Session().utilisateur.supprimer_scene_a_sd(
                id_sd=Session().sd_to_param.id_sd, id_scene=scene.id_scene
            )
        except (ValueError, AttributeError) as e:
            raise ValueError(f"La suppression de la scène n'a pas abouti : {e}")
        return True

    def modifier_nom_scene(self, scene: Scene, new_nom: str, schema: str):
        # On update la session
        scene.modifier_nom(nouveau_nom=new_nom)
        # On update le user en session
        for sounddeck in Session().utilisateur.SD_possedes:
            for s in sounddeck.scenes:
                if s.id_scene == scene.id_scene:
                    s.modifier_nom(nouveau_nom=new_nom)
        # On update la BDD
        SceneDAO().modifier_scene(scene=scene, schema=schema)

    def modifier_desc_scene(self, scene: Scene, new_desc: str, schema: str):
        # On update la session
        scene.modifier_description(nouvelle_description=new_desc)
        # On update le user en session
        for sounddeck in Session().utilisateur.SD_possedes:
            for s in sounddeck.scenes:
                if s.id_scene == scene.id_scene:
                    s.modifier_description(nouvelle_description=new_desc)
        # On update la BDD
        SceneDAO().modifier_scene(scene=scene, schema=schema)


"""
    @log
    def creer(**kwargs):
        "Création d'une scène à partir de ses attributs"
        new_scene = Scene(**kwargs)
        return new_scene if SceneDAO().ajouter_scene(new_scene) else None

    @log
    def supprimer(self, scene) -> bool:
        "Supprimme une scene"
        return SceneDAO().supprimer(scene)

    @log
    def modifier_nom(self, scene, new_name):
        pass

    @log
    def modifier_description(self, scene, new_desc):
        pass

    @log
    def ajouter_son_aleatoire(self, scene, new_son_aleatoire):
        pass

    @log
    def ajouter_son_manuel(self, scene, new_son_manuel):
        pass

    @log
    def ajouter_son_continu(self, scene, new_son_continu):
        pass

    @log
    def modifier_son_aleatoire(self, scene, new_son_aleatoire):
        pass

    @log
    def modifier_son_manuel(self, scene, new_son_manuel):
        pass

    @log
    def modifier_son_continu(self, scene, new_son_continu):
        pass
"""
