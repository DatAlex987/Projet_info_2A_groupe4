import pygame


class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.couleur = (100, 200, 100)
        self.texte = texte
        self.police = pygame.font.SysFont(None, 24)
        self.est_arret = None

    def dessiner(self, screen):
        pygame.draw.rect(screen, self.couleur, self.rect)
        texte_surface = self.police.render(self.texte, True, (0, 0, 0))
        screen.blit(texte_surface, (self.rect.x + 10, self.rect.y + 10))

    def est_clique(self, position_souris):
        b = self.rect.collidepoint(position_souris)
        if self.est_arret is False and b:
            self.est_arret = True
        elif (self.est_arret is True or self.est_arret is None) and b:
            self.est_arret = False
        return b
