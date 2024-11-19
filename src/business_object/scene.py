from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_continu import Son_Continu
from business_object.son_manuel import Son_Manuel
import datetime
import os
import pygame


class Scene:
    """
    Classe représentant un scene : un groupement cohérent de son selon un lieu, une ambiance, etc...

    Attributs
    ----------
    nom : str
        nom
    description : str
        description
    id_scene : str
        identifiant de scene
    sons_aleatoires : list[Son_Aleatoire]
        liste des sons aléatoires présents dans la scène
    sons_continus : list[Son_Continu]
        liste des sons continus présents dans la scène
    sons_manuels : list[Son_Manuel]
        liste des sons manuels présents dans la scène
    date_creation : datetime.time
        Date de la création de la sound-deck
    """

    def __init__(
        self,
        nom,
        description,
        id_scene,
        sons_aleatoires,
        sons_manuels,
        sons_continus,
        date_creation,
    ):
        """Constructeur"""
        self.nom = nom
        self.description = description
        self.id_scene = id_scene
        self.sons_aleatoires: list[Son_Aleatoire] = sons_aleatoires
        self.sons_manuels: list[Son_Manuel] = sons_manuels
        self.sons_continus: list[Son_Continu] = sons_continus
        self.date_creation = date_creation

        if not isinstance(nom, str):
            raise TypeError("Le nom doit etre une instance de str.")
        if not isinstance(description, str):
            raise TypeError("La description doit être une instance de str.")
        if not isinstance(id_scene, str):
            raise TypeError("L'identifiant scène doit être une instance de string.")
        if not isinstance(sons_aleatoires, list):
            raise TypeError("La liste des sons aléatoires doit être une instance de list.")
        if not isinstance(sons_continus, list):
            raise TypeError("La liste des sons continus doit être une instance de list.")
        if not isinstance(sons_manuels, list):
            raise TypeError("La liste des sons manuels doit être une instance de list.")
        if not isinstance(date_creation, datetime.date):
            raise TypeError("La date de création doit être une instance de datetime.")

    def modifier_nom(self, nouveau_nom):
        """Modifier le nom de la scène"""
        if not isinstance(nouveau_nom, str):
            raise TypeError("Le nouveau nom doit etre une instance de str.")
        self.nom = nouveau_nom

    def modifier_description(self, nouvelle_description):
        """Modifier la description de la scène"""
        if not isinstance(nouvelle_description, str):
            raise TypeError("La nouvelle description doit etre une instance de str.")
        self.description = nouvelle_description

    def ajouter_son_aleatoire(self, nouveau_son_aleatoire: Son_Aleatoire):
        """Ajoute un nouveau son aléatoire dans la scène"""
        if not isinstance(nouveau_son_aleatoire, Son_Aleatoire):
            raise TypeError("Le nouveau son doit etre une instance de son aléatoire.")
        self.sons_aleatoires.append(nouveau_son_aleatoire)

    def ajouter_son_continu(self, nouveau_son_continu: Son_Continu):
        """Ajoute un nouveau son continu dans la scène"""
        if not isinstance(nouveau_son_continu, Son_Continu):
            raise TypeError("Le nouveau son doit etre une instance de son continu.")
        self.sons_continus.append(nouveau_son_continu)

    def ajouter_son_manuel(self, nouveau_son_manuel: Son_Manuel):
        """Ajoute un nouveau son manuel dans la scène"""
        if not isinstance(nouveau_son_manuel, Son_Manuel):
            raise TypeError("Le nouveau son doit etre une instance de son manuel.")
        self.sons_manuels.append(nouveau_son_manuel)

    def supprimer_son_aleatoire(self, son_aleatoire: Son_Aleatoire):
        """Ajoute un nouveau son aléatoire dans la scène"""
        self.sons_aleatoires.remove(son_aleatoire)

    def supprimer_son_continu(self, son_continu: Son_Continu):
        """Ajoute un nouveau son continu dans la scène"""
        self.sons_continus.remove(son_continu)

    def supprimer_son_manuel(self, son_manuel: Son_Manuel):
        """Ajoute un nouveau son manuel dans la scène"""
        self.sons_manuels.remove(son_manuel)

    def supprimer_scene(self):
        del self
        return True

    def jouer_scene(self):
        """methode de jeu avec fenêtre interactive"""
        os.environ["SDL_VIDEO_WINDOW_POS"] = "100,50"
        # Initialisation de Pygame

        largeur = 1490
        hauteur = 400
        # Obtenir la taille de l'écran
        info_ecran = pygame.display.Info()
        largeur_ecran = info_ecran.current_w
        hauteur_ecran = info_ecran.current_h
        k = 97
        g = 89
        # Calculer la position pour centrer la fenêtre
        position_x = (largeur_ecran - largeur) // 2 + g
        position_y = (hauteur_ecran - hauteur) // 2 - k

        # Définir la position de la fenêtre
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{position_x},{position_y}"
        fenetre = pygame.display.set_mode((largeur, hauteur))
        # Définir le titre de la fenêtre
        pygame.display.set_caption("DM Sound buddy window")
        for sc in self.sons_continus:
            sc.localise_son()
            pygame.mixer.load(sc)

        # Définir les couleurs (R, G, B)
        BLANC = (255, 255, 255)
        NOIR = (0, 0, 0)
        ROUGE = (255, 0, 0)

        running = True
        while running:
            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        print("Espace pressé !")

        # Dessiner un fond de couleur unie
        fenetre.fill(BLANC)

        # Dessiner un rectangle (x, y, largeur, hauteur)
        pygame.draw.rect(fenetre, ROUGE, (300, 200, 200, 100))

        # Afficher du texte (optionnel)
        font = pygame.font.SysFont("Arial", 36)
        texte = font.render("Bonjour, Pygame !", True, NOIR)
        fenetre.blit(texte, (250, 50))

        # Afficher une image (optionnel)
        # fenetre.blit(image, (100, 100))

        # Mettre à jour l'affichage
        pygame.display.flip()
        pass
