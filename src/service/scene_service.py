from utils.log_decorator import log
from business_object.scene import Scene
from view.session import Session
import re
import datetime
import random
import string
from dao.scene_dao import SceneDAO


class SceneService:
    """Méthodes de service des scènes"""

    def input_checking_injection(self, nom: str, description: str):
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
        ???
        """
        print(
            "Scènes du SD au début de créer scène:",
            [scene.nom for sd in Session().utilisateur.SD_possedes for scene in sd.scenes],
        )
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
            print(
                "Scènes du SD à la fin de créer scène:",
                [scene.nom for sd in Session().utilisateur.SD_possedes for scene in sd.scenes],
            )
            return True
        except ValueError as e:
            raise ValueError(f"{e}")


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
