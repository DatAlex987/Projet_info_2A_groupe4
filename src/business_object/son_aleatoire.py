from business_object.son import Son
import pygame
import random


class Son_Aleatoire(Son):
    """
    Classe fille de Son qui permet de jouer un son de manière aléatoire sur une plage définie.

    Attributs
    ----------
    cooldown_min : int
        Temps minimum avant que le son soit rejoué.
    cooldown_max : int
        Temps maximum avant que le son soit rejoué.
    """

    def __init__(self, nom, description, duree, id_freesound, tags, cooldown_min, cooldown_max):
        super().__init__(nom, description, duree, id_freesound, tags)
        """Constructeur"""
        self.cooldown_min = cooldown_min
        self.cooldown_max = cooldown_max

    def modifier_cooldown(self, new_cooldown_min, new_cooldown_max):
        """Modifier les paramètres de cooldown d'un son aléatoire."""
        if not isinstance(new_cooldown_min, int) or not isinstance(new_cooldown_max, int):
            raise TypeError("Les cooldowns doivent être des entiers.")

        if new_cooldown_min < 0 or new_cooldown_max < 0:
            raise ValueError("Les cooldowns ne peuvent pas être négatifs.")

        if new_cooldown_min > new_cooldown_max:
            raise ValueError("Le cooldown minimum ne peut pas être supérieur au cooldown maximum.")

        self.cooldown_min = new_cooldown_min
        self.cooldown_max = new_cooldown_max

    def jouer_son_aléatoire(self):
        """Joue le son aléatoire comme attendu"""
        # Générer un délai initial aléatoire
        t = random.randint(self.cooldown_min, self.cooldown_max)
        pygame.time.delay(t)  # Attendre le délai initial avant de jouer le son

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.jouer_son()

            # Attendre que le son se termine (environ sa durée)
            # On suppose que le son ne change pas pendant l'exécution
            pygame.time.delay(int(self.charge.get_length() * 1000))  # Délai en millisecondes

            # Attendre un délai aléatoire avant de relancer le son
            t_prime = random.randint(self.cooldown_min, self.cooldown_max)
            pygame.time.delay(t_prime)
