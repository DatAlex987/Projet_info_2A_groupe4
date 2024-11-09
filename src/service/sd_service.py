import re
import datetime
import random
import string
from view.session import Session
from business_object.sd import SD
from business_object.scene import Scene
from business_object.son import Son
from business_object.son_continu import Son_Continu
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_manuel import Son_Manuel
from dao.sd_dao import SDDAO
from dao.scene_dao import SceneDAO


class SDService:
    """Classe contenant les méthodes de service des Sound-decks"""

    def input_checking_injection(self, nom: str, description: str):
        # Check inputs pour injection:
        # Définition de pattern regex pour qualifier les caractères acceptés pour chaque input
        pattern = r"^[a-zA-Zà-öø-ÿÀ-ÖØ-ß\s0-9\s,.\-:!@#%^&*()_+=|?/\[\]{}']*$"  # Autorise lettres, et autres caractères
        # On vérifie que les inputs sont conformes aux patternes regex.
        if not re.match(pattern, nom):
            raise ValueError("Le nom de la SD contient des caractères invalides.")
        if not re.match(pattern, description):
            raise ValueError("La description de la SD contient des caractères invalides.")

    @staticmethod  # Ne nécessite pas d'instance de SDService pour exister
    def id_sd_generator():
        """Génère un identifiant pour une SD.

        Identifiant de la forme XYZRSTU où X,Y,Z,R,S,T,U sont des caractères alphanumériques

        Returns:
        -------------------------
        str
            Identifiant (supposé unique) généré pour une SD.
        """
        generation = "".join(random.choices(string.ascii_letters + string.digits, k=7))
        unique_id = f"{generation}"
        return unique_id

    def creer_sd(self, nom: str, description: str, schema: str):
        """Instancie une SD avec les inputs de l'utilisateur et l'ajoute dans la BDD

        Param
        ------------
        nom : str
            nom donné à la SD par l'utilisateur
        description : str
            description donnée à la SD par l'utilisateur
        schema : str
            schema sur lequel opérer l'ajout de la SD

        Returns
        ------------
        ???
        """
        SDService().input_checking_injection(nom=nom, description=description)
        try:
            new_sd = SD(
                nom=nom,
                description=description,
                id_sd=SDService.id_sd_generator(),
                scenes=[],
                date_creation=datetime.datetime.today().date(),
            )
            SDDAO().ajouter_sd(sd=new_sd, schema=schema)
            SDDAO().ajouter_association_user_sd(
                id_user=Session().utilisateur.id_user, id_sd=new_sd.id_sd, schema=schema
            )
            Session().utilisateur.SD_possedes.append(new_sd)
            return True
        except ValueError as e:
            raise ValueError(f"{e}")

    def supprimer_sd(self, id_sd: str, schema: str):
        # Il faut trouver une solution aux pb soulevés sur whatsapp le 09/11 à 15h avant.
        """
        if SDDAO().supprimer_sd(id_sd=id_sd, schema=schema):
            SceneDAO().supprimer_association_sd_scene(id_sd=, id_scene=)
            SDDAO().supprimer_association_user_sd(id_user=, id_sd=, schema=schema)
        """

    def instancier_sd_par_id(self, id_sd: str, schema: str):
        sd_kwargs = SDDAO().rechercher_par_id_sd(id_sd=id_sd, schema=schema)
        Sons_Alea_scene = []
        Sons_Cont_scene = []
        Sons_Manu_scene = []
        for scene in sd_kwargs["scenes"]:
            for son_alea_kwargs in scene["sons_aleatoires"]:
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
        for scene in sd_kwargs["scenes"]:
            for son_cont_kwargs in scene["sons_continus"]:
                Sons_Cont_scene.append(
                    Son_Continu(
                        nom=son_cont_kwargs["nom"],
                        description=son_cont_kwargs["description"],
                        duree=son_cont_kwargs["duree"],
                        id_freesound=son_cont_kwargs["id_freesound"],
                        tags=son_alea_kwargs["tags"],
                    )
                )
        for scene in sd_kwargs["scenes"]:
            for son_manu_kwargs in scene["sons_manuels"]:
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
        Scenes_of_sd = []
        for scene_kwargs in sd_kwargs["scenes"]:
            Scenes_of_sd.append(
                Scene(
                    nom=scene_kwargs["nom"],
                    description=scene_kwargs["description"],
                    id_scene=scene_kwargs["id_scene"],
                    sons_aleatoires=Sons_Alea_scene,
                    sons_manuels=Sons_Manu_scene,
                    sons_continus=Sons_Cont_scene,
                    date_creation=scene_kwargs["date_creation"],
                )
            )
            sd = SD(
                nom=sd_kwargs["nom"],
                description=sd_kwargs["description"],
                id_sd=sd_kwargs["id_sd"],
                scenes=Scenes_of_sd,
                date_creation=sd_kwargs["date_creation"],
            )
        return sd

    def formatage_question_sds_of_user(self):
        sds_user = Session().utilisateur.SD_possedes
        choix = []
        compteur = 1
        for sd in sds_user:
            mise_en_page_ligne = f"{compteur}. {sd.id_sd} | {sd.nom} | {sd.description[:min(len(sd.description), 40)]}... | {sd.date_creation}"
            choix.append(mise_en_page_ligne)
            compteur += 1
        choix.append("Retour au menu de paramétrage")
        return choix
