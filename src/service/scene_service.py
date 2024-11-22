from business_object.scene import Scene
from business_object.son_continu import Son_Continu
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_manuel import Son_Manuel
from service.session import Session
from service.sd_service import SDService
from utils.Bouton import Bouton
from os import environ
import pygame
import datetime
import random
import string
from dao.scene_dao import SceneDAO
from dao.son_dao import SonDAO
from dao.tag_dao import TagDAO

####
from rich.console import Console
from rich.table import Table
from rich.style import Style


class SceneService:
    """Méthodes de service des scènes"""

    @staticmethod  # Ne nécessite pas d'instance de SceneService pour exister
    def id_scene_generator():
        """Génère un identifiant pour une scène.

        Identifiant de la forme XYZRSTU où X,Y,Z,R,S,T,U sont des caractères alphanumériques

        Returns:
        -------------------------
        str
            Identifiant (supposé unique) généré pour une Scène.
        """
        all_scenes = SceneDAO().consulter_scenes(schema="ProjetInfo")
        all_ids = [scene["id_scene"] for scene in all_scenes]
        generation = "".join(random.choices(string.ascii_letters + string.digits, k=7))
        unique_id = f"{generation}"
        while unique_id in all_ids:  # On vérifie que l'id n'existe pas déjà
            generation = "".join(random.choices(string.ascii_letters + string.digits, k=7))
            unique_id = f"{generation}"
        return unique_id

    def formatage_question_scenes_of_sd(self):
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
        choix = []
        compteur = 1
        for scene in Session().sd_to_param.scenes:
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
        SDService().input_checking_injection(input_str=nom)
        SDService().input_checking_injection(input_str=description)
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

    def formatage_question_scenes_of_sd_menu_jeu(self):
        choix = []
        compteur = 1
        for scene in Session().sd_to_play.scenes:
            mise_en_page_ligne = (
                f"{compteur}. {scene.id_scene} | {scene.nom} | {scene.date_creation}"
            )
            choix.append(mise_en_page_ligne)
            compteur += 1
        choix.append("Retour au menu de choix des sound-decks")
        return choix

    def formatage_question_scenes_of_sd_menu_consult(self):
        choix = []
        compteur = 1
        for scene in Session().sd_to_consult.scenes:
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
                    id_son=son_alea_kwargs["id_son"],
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
                    id_son=son_cont_kwargs["id_son"],
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
                    id_son=son_manu_kwargs["id_son"],
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
                    id_son=son.id_son, type_son="aleatoire", schema=schema
                )
                for tag in son.tags:
                    TagDAO().supprimer_association_son_tag(
                        id_son=son.id_son, tag=tag, schema=schema
                    )
            for son in scene.sons_continus:
                SonDAO().supprimer_toutes_associations_son(
                    id_son=son.id_son, type_son="continu", schema=schema
                )
                for tag in son.tags:
                    TagDAO().supprimer_association_son_tag(
                        id_son=son.id_son, tag=tag, schema=schema
                    )
            for son in scene.sons_manuels:
                SonDAO().supprimer_toutes_associations_son(
                    id_son=son.id_son, type_son="manuel", schema=schema
                )
                for tag in son.tags:
                    TagDAO().supprimer_association_son_tag(
                        id_son=son.id_son, tag=tag, schema=schema
                    )
            # On termine par actualiser la session
            Session().utilisateur.supprimer_scene_a_sd(
                id_sd=Session().sd_to_param.id_sd, id_scene=scene.id_scene
            )
        except (ValueError, AttributeError) as e:
            raise ValueError(f"La suppression de la scène n'a pas abouti : {e}")
        return True

    def modifier_nom_scene(self, scene: Scene, new_nom: str, schema: str):
        SDService().input_checking_injection(input_str=new_nom)
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
        SDService().input_checking_injection(input_str=new_desc)
        # On update la session
        scene.modifier_description(nouvelle_description=new_desc)
        # On update le user en session
        for sounddeck in Session().utilisateur.SD_possedes:
            for s in sounddeck.scenes:
                if s.id_scene == scene.id_scene:
                    s.modifier_description(nouvelle_description=new_desc)
        # On update la BDD
        SceneDAO().modifier_scene(scene=scene, schema=schema)

    def afficher_details_scene(self, scene):
        """Affiche les détails d'un son aléatoire."""
        console = Console()
        table = Table(
            show_header=True,
            header_style=Style(color="chartreuse1", bold=True),
            title="--------------- Détails de la scène ---------------",
            style="white",
        )
        table.add_column("Champ", style=Style(color="honeydew2"), width=20)
        table.add_column("Détails", style=Style(color="honeydew2"))
        table.add_row("ID de scène", str(scene.id_scene))
        table.add_row("Nom", scene.nom)
        table.add_row("description", str(scene.description))
        table.add_row("Date de création", str(scene.date_creation))

        console.print(table)

    def jouer_scene(self, scene: Scene):
        """methode de jeu avec fenêtre interactive"""
        # Initialisation de Pygame
        pygame.init()
        pygame.mixer.init()

        largeur = 1490
        hauteur = 400
        # Obtenir la taille de l'écran
        info_ecran = pygame.display.Info()
        largeur_ecran = info_ecran.current_w
        hauteur_ecran = info_ecran.current_h
        k = 97
        g = 89
        # Calcul de la position pour centrer la fenêtre
        position_x = (largeur_ecran - largeur) // 2 + g
        position_y = (hauteur_ecran - hauteur) // 2 - k

        dictb = {"continus": [], "alea": [], "manuels": []}
        bouton_continu_actif = []  # suivi du son actif continu
        bouton_continu_actif.append(Bouton(0, 0, 0, 0, "_", "continu"))
        x_position = 50
        x_position_2 = 50
        x_position_3 = 50
        # Création des boutons pour les sons continus
        for son in scene.sons_manuels:
            dictb["manuels"].append(
                (
                    Bouton(
                        x_position_3,
                        300,
                        150,
                        40,
                        f"{son.nom[:12]}... , {son.start_key.upper()}",
                        "manuel",
                        couleur=(173, 216, 230),
                    ),
                    son,
                )
            )
            x_position_3 += 170
            fp = son.localise_son()
            son.charge = pygame.mixer.Sound(fp)

        for son in scene.sons_continus:
            dictb["continus"].append(
                (Bouton(x_position, 100, 150, 40, f"{son.nom[:13]}...", "continu"), son)
            )
            x_position += 170
            fp = son.localise_son()
            pygame.mixer.music.load(fp)
        # Création des boutons pour les sons aléatoires
        longueur_sons_aleatoires = len(scene.sons_aleatoires)
        for k, son in enumerate(scene.sons_aleatoires):
            dictb["alea"].append(
                (Bouton(x_position_2, 200, 150, 40, f"{son.nom[:13]}", "aleatoire"), son)
            )
            fp = son.localise_son()
            son.charge = pygame.mixer.Sound(fp)
            son.event_son = pygame.USEREVENT + (k + 1)
            x_position_2 += 170

        # Définir la position de la fenêtre
        environ["SDL_VIDEO_WINDOW_POS"] = f"{position_x},{position_y}"
        fenetre = pygame.display.set_mode((largeur, hauteur))
        # Définir le titre de la fenêtre
        pygame.display.set_caption("DM Sound buddy window")

        NOIR = (0, 0, 0)
        BEIGE = (245, 222, 179)
        # Dessiner un fond de couleur noire
        fenetre.fill(BEIGE)
        font = pygame.font.Font(None, 74)  # Taille de la police : 74
        texte_1_surface = font.render("Tableau de contrôle", True, NOIR)
        texte_2_surface = font.render("Sons continus", True, NOIR)
        texte_3_surface = font.render("Sons aleatoires", True, NOIR)
        texte_3_surface = font.render("Sons aleatoires", True, NOIR)
        texte_4_surface = font.render("Sons manuels", True, NOIR)
        # Obtenir la taille et la position du texte
        texte_1_rect = texte_1_surface.get_rect(center=(largeur // 2, 50))
        texte_2_rect = texte_2_surface.get_rect(topleft=(50, 50))
        texte_3_rect = texte_3_surface.get_rect(topleft=(50, 150))
        texte_4_rect = texte_4_surface.get_rect(topleft=(50, 250))

        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    for bouton, son in dictb["manuels"]:
                        if event.key == son.convert_to_kpg(son.start_key):
                            son.jouer_Son()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position_souris = pygame.mouse.get_pos()
                    for bouton, son in dictb["continus"]:
                        if bouton.est_clique(position_souris):
                            if bouton.couleur == (200, 100, 100):
                                son.Arret_Son()
                            if bouton.couleur == (100, 200, 100):
                                son.jouer_Son()
                                bouton_continu_actif[0].couleur = (200, 100, 100)
                                bouton_continu_actif.clear()
                                bouton_continu_actif.append(bouton)
                    for bouton, son in dictb["alea"]:
                        if bouton.est_clique(position_souris):
                            if bouton.couleur == (200, 100, 100):
                                son.Arret_Son()
                            if bouton.couleur == (100, 200, 100):
                                son.jouer_Son()
                elif (
                    pygame.USEREVENT + 1
                    <= event.type
                    <= pygame.USEREVENT + longueur_sons_aleatoires
                ):
                    j = event.type - pygame.USEREVENT  # Calculer le numéro du son
                    for son in scene.sons_aleatoires:
                        if son.event_son - pygame.USEREVENT == j:
                            son.charge.play()

            for bouton, r in dictb["continus"]:
                bouton.dessiner(fenetre)
            for bouton, r in dictb["alea"]:
                bouton.dessiner(fenetre)
            for bouton, r in dictb["manuels"]:
                bouton.dessiner(fenetre)

            fenetre.blit(texte_1_surface, texte_1_rect)
            fenetre.blit(texte_2_surface, texte_2_rect)
            fenetre.blit(texte_3_surface, texte_3_rect)
            fenetre.blit(texte_4_surface, texte_4_rect)
            pygame.display.flip()

        pygame.mixer.stop()
        pygame.quit()
