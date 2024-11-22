import re
import datetime
import random
import string
from service.session import Session

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

####
from rich.console import Console
from rich.table import Table
from rich.style import Style


class SDService:
    """Classe contenant les méthodes de service des Sound-decks"""

    def input_checking_injection(self, input_str: str):
        """
        Vérifie qu'une chaîne de caractères n'est pas une injection SQL

        Param
        ---------------
        input_str : str
            La chaîne de caractères à tester
        """
        # Patterns pour éviter les injections SQL
        patterns = [
            r"(--|#)",  # Commentaires
            r"(\bUNION\b)",  # UNION
            r"(;|\bDROP\b|\bDELETE\b|\bINSERT\b|\bUPDATE\b|\bSELECT\b)",  # CRUD
            r"(\')",  # guillemet simple
            r"(\bEXEC\b|\bEXECUTE\b)",  # EXECUTE
        ]

        # Pour chaque pattern, on vérifie que l'input est correct
        for pattern in patterns:
            if re.search(pattern, input_str, re.IGNORECASE):
                raise ValueError(
                    f"La chaîne de caractère {input_str} comporte des caracètres invalides"
                )

    @staticmethod  # Ne nécessite pas d'instance de SDService pour exister
    def id_sd_generator():
        """Génère un identifiant pour une SD.

        Identifiant de la forme XYZRSTU où X,Y,Z,R,S,T,U sont des caractères alphanumériques

        Returns:
        -------------------------
        str
            Identifiant (supposé unique) généré pour une SD.
        """
        all_sds = SDDAO().consulter_sds(schema="ProjetInfo")
        all_ids = [sd["id_sd"] for sd in all_sds]
        generation = "".join(random.choices(string.ascii_letters + string.digits, k=7))
        unique_id = f"{generation}"
        while unique_id in all_ids:  # On vérifie que l'id n'existe pas déjà
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
        SDService().input_checking_injection(input_str=nom)
        SDService().input_checking_injection(input_str=description)
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
                    SonDAO().supprimer_toutes_associations_son(id_son=son.id_son, schema=schema)
                    for tag in son.tags:
                        TagDAO().supprimer_association_son_tag(
                            id_son=son.id_son, tag=tag, schema=schema
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
        for scene in sd_kwargs["scenes"]:
            # Ces 3 init de listes étaient juste avant le for avant de régler le pb
            Sons_Alea_scene = []
            Sons_Cont_scene = []
            Sons_Manu_scene = []
            for son_alea_kwargs in scene["sons_aleatoires"]:
                Sons_Alea_scene.append(
                    Son_Aleatoire(
                        nom=son_alea_kwargs["nom"],
                        description=son_alea_kwargs["description"],
                        duree=son_alea_kwargs["duree"],
                        id_freesound=son_alea_kwargs["id_freesound"],
                        id_son=son_alea_kwargs["id_son"],
                        tags=son_alea_kwargs["tags"],
                        cooldown_min=son_alea_kwargs["param1"],
                        cooldown_max=son_alea_kwargs["param2"],
                    )
                )
            for son_cont_kwargs in scene["sons_continus"]:
                Sons_Cont_scene.append(
                    Son_Continu(
                        nom=son_cont_kwargs["nom"],
                        description=son_cont_kwargs["description"],
                        duree=son_cont_kwargs["duree"],
                        id_freesound=son_cont_kwargs["id_freesound"],
                        id_son=son_cont_kwargs["id_son"],
                        tags=son_cont_kwargs["tags"],
                    )
                )
            for son_manu_kwargs in scene["sons_manuels"]:
                Sons_Manu_scene.append(
                    Son_Manuel(
                        nom=son_manu_kwargs["nom"],
                        description=son_manu_kwargs["description"],
                        duree=son_manu_kwargs["duree"],
                        id_freesound=son_manu_kwargs["id_freesound"],
                        id_son=son_manu_kwargs["id_son"],
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
        SDService().input_checking_injection(input_str=new_nom)
        # On update la session
        sd.modifier_nom_sd(nouveau_nom=new_nom)
        # On update le user en session
        for sounddeck in Session().utilisateur.SD_possedes:
            if sounddeck.id_sd == sd.id_sd:
                sounddeck.modifier_nom_sd(nouveau_nom=new_nom)
        # On update la BDD
        SDDAO().modifier_sd(sd=sd, schema=schema)

    def modifier_desc_sd(self, sd: SD, new_desc: str, schema: str):
        SDService().input_checking_injection(input_str=new_desc)
        # On update la session
        sd.modifier_description_sd(nouvelle_description=new_desc)
        # On update le user en session
        for sounddeck in Session().utilisateur.SD_possedes:
            if sounddeck.id_sd == sd.id_sd:
                sounddeck.modifier_description_sd(nouvelle_description=new_desc)
        # On update la BDD
        SDDAO().modifier_sd(sd=sounddeck, schema=schema)

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
            table.add_row(
                str(idx),
                sd.id_sd,
                sd.nom,
                sd.description[:40] + ("..." if len(sd.description) > 40 else ""),
                sd.date_creation,
            )
        return table

    def obtenir_choices_sds_user(self):
        """
        Renvoie une liste des choix formatés pour InquirerPy.
        """
        sds_user = Session().utilisateur.SD_possedes
        return [f"{idx}. {sd.id_sd}" for idx, sd in enumerate(sds_user, start=1)]

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

    def ajouter_sd_existante_to_user(self, schema: str):  # NOT TESTED YET
        try:
            Session().utilisateur.ajouter_sd(sd=Session().sd_to_consult)
            SDDAO().ajouter_association_user_sd(
                id_user=Session().utilisateur.id_user,
                id_sd=Session().sd_to_consult.id_sd,
                schema=schema,
            )
        except ValueError as e:
            raise ValueError(f"Erreur lors de la sauvegarde de la sound-deck: {e}")

    def dupliquer_sd_existante_to_user(self, schema: str):
        from service.son_service import SonService  # Pour éviter circular imports
        from service.scene_service import SceneService  # Pour éviter circular imports

        # On change l'id du créateur pour permettre à l'utilisateur de faire des modifications
        # à l'avenir sur cette SD
        # Pour chaque objet, on ajoute l'objet et on créé les associations son/tag.

        # On duplique la SD puis on l'ajoute

        sd_to_dupli = Session().sd_to_consult
        sd_duplicated = SD(
            id_sd=SDService.id_sd_generator(),
            nom=sd_to_dupli.nom,
            description=sd_to_dupli.description,
            scenes=[],  # Pas important pour l'ajout en BDD
            date_creation=datetime.datetime.today().date(),  # Date d'aujourd'hui
            id_createur=Session().utilisateur.id_user,  # Duplication, donc pour avoir les droits, il devient créateur.
        )
        SDDAO().ajouter_sd(sd=sd_duplicated, schema=schema)
        dict_of_associations_scene_son = {}
        for scene in sd_to_dupli.scenes:  # Pour chaque scène...
            print("sons alea dans scène:", scene.sons_aleatoires)
            # On duplique la Scène puis on l'ajoute
            scene_duplicated = Scene(
                nom=scene.nom,
                description=scene.description,
                id_scene=SceneService().id_scene_generator(),
                sons_aleatoires=[],  # Pas important pour l'ajout en BDD
                sons_continus=[],  # Pas important pour l'ajout en BDD
                sons_manuels=[],  # Pas important pour l'ajout en BDD
                date_creation=datetime.datetime.today().date(),
            )
            SceneDAO().ajouter_scene(scene=scene_duplicated, schema=schema)
            dict_of_associations_scene_son[scene_duplicated] = []
            for son_alea in scene.sons_aleatoires:  # ... on instancie le son dupliqué
                print("id son alea a dupliquer:", son_alea.id_son)
                # On duplique le son puis on l'ajoute
                son_duplicated = Son_Aleatoire(
                    nom=son_alea.nom,
                    description=son_alea.description,
                    duree=son_alea.duree,
                    id_son=SonService.id_son_generator(),
                    id_freesound=son_alea.id_freesound,
                    tags=son_alea.tags,
                    cooldown_min=son_alea.cooldown_min,
                    cooldown_max=son_alea.cooldown_max,
                )
                SonDAO().ajouter_son(son=son_duplicated, schema=schema)  # ... on l'ajoute en BDD
                for tag in son_duplicated.tags:  # ... on ajoute ses associations son/tags
                    TagDAO().ajouter_association_son_tag(
                        id_son=son_duplicated.id_son, tag=tag, schema=schema
                    )
                dict_of_associations_scene_son[scene_duplicated].append(
                    son_duplicated
                )  # ... et on garde une trace pour ajouter les associations scene/son juste après.
            for son_continu in scene.sons_continus:
                son_duplicated = Son_Continu(
                    nom=son_continu.nom,
                    description=son_continu.description,
                    duree=son_continu.duree,
                    id_son=SonService.id_son_generator(),
                    id_freesound=son_continu.id_freesound,
                    tags=son_continu.tags,
                )
                SonDAO().ajouter_son(son=son_duplicated, schema=schema)
                for tag in son_duplicated.tags:
                    TagDAO().ajouter_association_son_tag(
                        id_son=son_duplicated.id_son, tag=tag, schema=schema
                    )
                dict_of_associations_scene_son[scene_duplicated].append(son_duplicated)
            for son_manuel in scene.sons_manuels:
                son_duplicated = Son_Manuel(
                    nom=son_manuel.nom,
                    description=son_manuel.description,
                    duree=son_manuel.duree,
                    id_son=SonService.id_son_generator(),
                    id_freesound=son_manuel.id_freesound,
                    tags=son_manuel.tags,
                    start_key=son_manuel.start_key,
                )
                SonDAO().ajouter_son(son=son_duplicated, schema=schema)
                for tag in son_duplicated.tags:
                    TagDAO().ajouter_association_son_tag(
                        id_son=son_duplicated.id_son, tag=tag, schema=schema
                    )
                dict_of_associations_scene_son[scene_duplicated].append(son_duplicated)

        # On ajoute toutes les associations (scene/son):
        for scene, sons in dict_of_associations_scene_son.items():
            for son in sons:
                SonDAO().ajouter_association_scene_son(
                    id_scene=scene.id_scene, son=son, schema=schema
                )

        # Puis on ajoute les associations SD/Scenes
        for scene in dict_of_associations_scene_son.keys():
            SceneDAO().ajouter_association_sd_scene(
                id_sd=sd_duplicated.id_sd, id_scene=scene.id_scene, schema=schema
            )
        # Puis on ajoute l'association User/SD:
        SDDAO().ajouter_association_user_sd(
            id_user=Session().utilisateur.id_user, id_sd=sd_duplicated.id_sd, schema=schema
        )

        # Enfin, on actualise la session:
        new_sd = SDService().instancier_sd_par_id(id_sd=sd_duplicated.id_sd, schema=schema)
        Session().utilisateur.ajouter_sd(sd=new_sd)

    def afficher_details_sd(self, sd):
        """Affiche les détails d'un son aléatoire."""
        console = Console()
        table = Table(
            show_header=True,
            header_style=Style(color="chartreuse1", bold=True),
            title="--------------- Détails de la sound-deck ---------------",
            style="white",
        )
        table.add_column("Champ", style=Style(color="honeydew2"), width=20)
        table.add_column("Détails", style=Style(color="honeydew2"))
        table.add_row("ID de sound-deck", str(sd.id_sd))
        table.add_row("Nom", sd.nom)
        table.add_row("description", str(sd.description))
        table.add_row("Date de création", str(sd.date_creation))
        table.add_row("ID Créateur", str(sd.id_createur))

        console.print(table)
