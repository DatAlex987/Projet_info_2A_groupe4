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
from dao.son_dao import SonDAO
from dao.tag_dao import TagDAO
from rich.table import Table


class SDService:
    """Classe contenant les méthodes de service des Sound-decks"""

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
                id_createur=Session().utilisateur.id_user,
            )
            SDDAO().ajouter_sd(sd=new_sd, schema=schema)
            SDDAO().ajouter_association_user_sd(
                id_user=Session().utilisateur.id_user, id_sd=new_sd.id_sd, schema=schema
            )
            Session().utilisateur.ajouter_sd(sd=new_sd)
            return True
        except ValueError as e:
            raise ValueError(f"{e}")

    def supprimer_sd(
        self, sd: SD, schema: str
    ):  # On a besoin de l'objet en entier pour supprimer en "cascade"
        # La suppression d'une SD supprime l'objet + toutes les associations dans les tables +
        # les associations en cascade. Mais pas les objets en cascade (car ils peuvent tjrs
        # exister dans d'autres SD)
        """Supprime une SD dans la BDD ainsi que toutes les associations qui en découlent

        Params
        -------------
        sd : SD
            SD à supprimer
        schema : str
            Schema sur lequel opérer la suppression

        Returns
        -------------
        bool
            True si la suppression n'a pas soulevé d'erreur, rien sinon
        """
        try:
            SDDAO().supprimer_sd(id_sd=sd.id_sd, schema=schema)
            SDDAO().supprimer_toutes_associations_sd(id_sd=sd.id_sd, schema=schema)
            for scene in sd.scenes:
                SceneDAO().supprimer_toutes_associations_scene(
                    id_scene=scene.id_scene, schema=schema
                )
                for son in scene.sons_aleatoires + scene.sons_continus + scene.sons_manuels:
                    SonDAO().supprimer_toutes_associations_son(
                        id_freesound=son.id_freesound, schema=schema
                    )
                    for tag in son.tags:
                        TagDAO().supprimer_association_son_tag(
                            id_freesound=son.id_freesound, tag=tag, schema=schema
                        )
            # On termine par actualiser la session
            Session().utilisateur.enlever_sd(sd=sd)
        except (ValueError, AttributeError) as e:
            raise ValueError(f"La suppression du SD n'a pas abouti : {e}")
        return True

    def instancier_sd_par_id(self, id_sd: str, schema: str):
        """Instancie un SD (et toutes les scènes, sons qui la composent) à partir de son id

        Params
        -------------
        id_sd : str
            id de la SD sélectionnée par l'utilisateur
        schema : str
            Schéma sur lequel faire les requêtes
        Returns
        -------------
        SD
            Instance de la SD demandée
        """
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
                        cooldown_min=son_alea_kwargs["param1"],
                        cooldown_max=son_alea_kwargs["param2"],
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
                        tags=son_cont_kwargs["tags"],
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
                        tags=son_manu_kwargs["tags"],
                        start_key=son_manu_kwargs["param1"],
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
            id_createur=sd_kwargs["id_createur"],
        )
        return sd

    def formatage_question_sds_of_user(self):
        """Construit une liste des choix à afficher dans le menu des SD param

        Returns
        -------------
        list
            Liste des choix proposés à l'utilisateur, incluant tous ses SD
        """
        sds_user = Session().utilisateur.SD_possedes
        choix = []
        compteur = 1
        for sd in sds_user:
            mise_en_page_ligne = f"{compteur}. {sd.id_sd} | {sd.nom} | {sd.description[:min(len(sd.description), 40)]}... | {sd.date_creation}"
            choix.append(mise_en_page_ligne)
            compteur += 1
        choix.append("Retour au menu de paramétrage")
        return choix

    def formatage_question_sds_of_user_menu_jeu(self):
        sds_user = Session().utilisateur.SD_possedes
        choix = []
        compteur = 1
        for sd in sds_user:
            mise_en_page_ligne = f"{compteur}. {sd.id_sd} | {sd.nom} | {sd.description[:min(len(sd.description), 40)]}... | {sd.date_creation}"
            choix.append(mise_en_page_ligne)
            compteur += 1
        choix.append("Retour au menu principal")
        return choix

    def modifier_nom_sd(self, sd: SD, new_nom: str, schema: str):
        # On update la session
        sd.modifier_nom_sd(nouveau_nom=new_nom)
        # On update le user en session
        for sounddeck in Session().utilisateur.SD_possedes:
            if sounddeck.id_sd == sd.id_sd:
                sounddeck.modifier_nom_sd(nouveau_nom=new_nom)
        # On update la BDD
        SDDAO().modifier_sd(sd=sd, schema=schema)

    def modifier_desc_sd(self, sd: SD, new_desc: str, schema: str):
        # On update la session
        sd.modifier_description_sd(nouvelle_description=new_desc)
        # On update le user en session
        for sounddeck in Session().utilisateur.SD_possedes:
            if sounddeck.id_sd == sd.id_sd:
                sounddeck.modifier_description_sd(nouvelle_description=new_desc)
        # On update la BDD
        SDDAO().modifier_sd(sd=sounddeck, schema=schema)

    def FindCloseNameSDs(self, nom_approx: str, schema: str):
        all_sds = SDDAO().consulter_sds(schema=schema)
        sds_close_name = []
        for sd in all_sds:
            if nom_approx.lower() in sd["nom"].lower():
                sds_close_name.append(self.instancier_sd_par_id(id_sd=sd["id_sd"], schema=schema))
        Session().sds_to_consult = sds_close_name

    def formatage_question_sds_to_consult(self):
        """Construit une liste des choix à afficher dans le menu des SD à consulter

        Returns
        -------------
        list
            Liste des choix proposés à l'utilisateur, incluant tous les SDs qui
            correspondent à sa recherche.
        """
        if Session().type_recherche_consult == "nom":
            sds_to_display = Session().sds_to_consult
            choix = []
            compteur = 1
            for sd in sds_to_display:
                mise_en_page_ligne = f"{compteur}. {sd.id_sd} | {sd.nom} | {sd.description[:min(len(sd.description), 40)]}... | {sd.date_creation}"
                choix.append(mise_en_page_ligne)
                compteur += 1
            choix.append("Retour au menu de recherche de consultation")
            return choix
        elif Session().type_recherche_consult == "user":
            sds_to_display = Session().user_to_consult.SD_possedes
            choix = []
            compteur = 1
            for sd in sds_to_display:
                mise_en_page_ligne = f"{compteur}. {sd.id_sd} | {sd.nom} | {sd.description[:min(len(sd.description), 40)]}... | {sd.date_creation}"
                choix.append(mise_en_page_ligne)
                compteur += 1
            choix.append("Retour au menu de recherche de consultation")
            return choix

    # TEST PAS ENCORE FONCTIONNEL NE PAS ENLEVER CEST POUR LES TABLEAUX :

    def afficher_tableau_sds_user(self):
        """
        Affiche un tableau Rich contenant les Sounddecks de l'utilisateur.
        """
        sds_user = Session().utilisateur.SD_possedes
        table = Table(title="Liste des Sounddecks disponibles")
        table.add_column("Index", justify="center")
        table.add_column("ID", justify="center")
        table.add_column("Nom", justify="left")
        table.add_column("Description", justify="left")
        table.add_column("Date de création", justify="center")

        for idx, sd in enumerate(sds_user, start=1):
            # Conversion de la date en chaîne
            date_creation_str = sd.date_creation.strftime("%Y-%m-%d") if sd.date_creation else "N/A"
            table.add_row(
                str(idx),
                sd.id_sd,
                sd.nom,
                sd.description[:40] + ("..." if len(sd.description) > 40 else ""),
                date_creation_str,
            )
        return table

    def obtenir_choices_sds_user(self):
        """
        Renvoie une liste des choix formatés pour InquirerPy.
        """
        sds_user = Session().utilisateur.SD_possedes
        return [f"{idx}. {sd.id_sd}" for idx, sd in enumerate(sds_user, start=1)]
