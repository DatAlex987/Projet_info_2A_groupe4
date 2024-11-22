import pygame


class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte, type_son, couleur=(200, 100, 100)):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.couleur = couleur
        self.texte = texte
        self.police = pygame.font.SysFont(None, 24)
        self.type_son = type_son

    def dessiner(self, screen):
        pygame.draw.rect(screen, self.couleur, self.rect, border_radius=15)
        texte_surface = self.police.render(self.texte, True, (0, 0, 0))
        screen.blit(texte_surface, (self.rect.x + 10, self.rect.y + 10))

    def est_clique(self, position_souris):
        b = self.rect.collidepoint(position_souris)
        if self.couleur == (100, 200, 100) and b:
            self.couleur = (200, 100, 100)
        elif self.couleur == (200, 100, 100) and b:
            self.couleur = (100, 200, 100)
        return b
