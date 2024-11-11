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

    def instancier_scene_par_id(self, id_scene: str, schema: str):
        scene_kwargs = SceneDAO().rechercher_par_id_scene(id_scene=id_scene, schema=schema)
        print("scene_kwargs:", scene_kwargs)
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
                    cooldown_min=son_alea_kwargs["cooldown_min"],
                    cooldown_max=son_alea_kwargs["cooldown_max"],
                )
            )
        print("Sons_Alea_scene:", Sons_Alea_scene)
        for son_cont_kwargs in scene_kwargs["sons_continus"]:
            Sons_Cont_scene.append(
                Son_Continu(
                    nom=son_cont_kwargs["nom"],
                    description=son_cont_kwargs["description"],
                    duree=son_cont_kwargs["duree"],
                    id_freesound=son_cont_kwargs["id_freesound"],
                    tags=son_alea_kwargs["tags"],
                )
            )
        for son_manu_kwargs in scene_kwargs["sons_manuels"]:
            Sons_Manu_scene.append(
                Son_Manuel(
                    nom=son_manu_kwargs["nom"],
                    description=son_manu_kwargs["description"],
                    duree=son_manu_kwargs["duree"],
                    id_freesound=son_manu_kwargs["id_freesound"],
                    tags=son_alea_kwargs["tags"],
                    start_key=son_manu_kwargs["start_key"],
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
        print("Scene_to_return:", scene_to_return)
        return scene_to_return


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
