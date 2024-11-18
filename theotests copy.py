import pygame
import random
import time

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
LARGEUR_FENETRE, HAUTEUR_FENETRE = 800, 600


class Son_continu:
    def __init__(self, fichier):
        self.son = pygame.mixer.Sound(fichier)
        self.jouer_son = False

    def jouer(self):
        if not self.jouer_son:
            self.son.play(loops=-1)  # Boucle infinie
            self.jouer_son = True

    def arreter(self):
        self.son.stop()
        self.jouer_son = False


class Son_aleatoire:
    def __init__(self, fichier, min_intervalle=1, max_intervalle=5):
        self.son = pygame.mixer.Sound(fichier)
        self.min_intervalle = min_intervalle
        self.max_intervalle = max_intervalle
        self.dernier_temps = time.time()
        self.intervalle = random.uniform(self.min_intervalle, self.max_intervalle)
        self.jouer_son = False

    def jouer(self):
        if self.jouer_son:
            temps_actuel = time.time()
            if temps_actuel - self.dernier_temps > self.intervalle:
                self.son.play()
                self.dernier_temps = temps_actuel
                self.intervalle = random.uniform(self.min_intervalle, self.max_intervalle)

    def arreter(self):
        self.jouer_son = False


class Son_manuel:
    def __init__(self, fichier, touche):
        self.son = pygame.mixer.Sound(fichier)
        self.touche = touche

    def jouer(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == self.touche:
                self.son.play()

    def arreter(self):
        self.son.stop()


class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.couleur = (100, 200, 100)
        self.texte = texte
        self.police = pygame.font.SysFont(None, 24)

    def dessiner(self, screen):
        pygame.draw.rect(screen, self.couleur, self.rect)
        texte_surface = self.police.render(self.texte, True, (0, 0, 0))
        screen.blit(texte_surface, (self.rect.x + 10, self.rect.y + 10))

    def est_clique(self, position_souris):
        return self.rect.collidepoint(position_souris)


class Scene:
    def __init__(self, sons_continus=None, sons_aleas=None, sons_manuels=None):
        self.sons_continus = sons_continus if sons_continus else []
        self.sons_aleas = sons_aleas if sons_aleas else []
        self.sons_manuels = sons_manuels if sons_manuels else []

    def jouer_scène(self):
        # Initialiser la fenêtre
        screen = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
        pygame.display.set_caption("Scène Sonore avec Boutons")
        clock = pygame.time.Clock()

        # Créer les boutons pour chaque son
        boutons = []
        y_position = 50

        # Création des boutons pour les sons continus
        for son in self.sons_continus:
            boutons.append((Bouton(50, y_position, 100, 40, "Jouer"), son.jouer))
            boutons.append((Bouton(200, y_position, 100, 40, "Arrêter"), son.arreter))
            y_position += 60

        # Création des boutons pour les sons aléatoires
        for son in self.sons_aleas:
            boutons.append(
                (
                    Bouton(50, y_position, 100, 40, "Jouer"),
                    lambda s=son: setattr(s, "jouer_son", True),
                )
            )
            boutons.append((Bouton(200, y_position, 100, 40, "Arrêter"), son.arreter))
            y_position += 60

        # Boucle principale pour la scène
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position_souris = pygame.mouse.get_pos()
                    for bouton, action in boutons:
                        if bouton.est_clique(position_souris):
                            action()

            # Mise à jour des sons aléatoires
            for son in self.sons_aleas:
                son.jouer()

            # Rafraîchir l'écran
            screen.fill((255, 255, 255))
            for bouton, _ in boutons:
                bouton.dessiner(screen)
            pygame.display.flip()

            # Limiter la boucle à 60 FPS
            clock.tick(60)

        pygame.mixer.stop()
        pygame.quit()


# Exemple d'utilisation
if __name__ == "__main__":
    son_continu = Son_continu("chemin/vers/son_continu.wav")
    son_aleatoire = Son_aleatoire(
        "chemin/vers/son_aleatoire.wav", min_intervalle=2, max_intervalle=4
    )

    # Créer une scène
    ma_scene = Scene(
        sons_continus=[son_continu],
        sons_aleas=[son_aleatoire],
    )

    # Jouer la scène
    ma_scene.jouer_scène()
