from business_object.son import Son
import pygame
import random


class Son_Aleatoire(Son):
    """
    Classe fille de Son qui permet de jouer un son de manière aléatoire sur une plage définie.

    Attributs
    ----------
    cooldown_min : int
        Temps minimum en secondes avant que le son soit rejoué.
    cooldown_max : int
        Temps maximum en secondes avant que le son soit rejoué.
    """

    def __init__(self, nom, description, duree, id_freesound, tags, cooldown_min, cooldown_max):
        super().__init__(nom, description, duree, id_freesound, tags)
        """Constructeur"""
        self.cooldown_min = cooldown_min
        self.cooldown_max = cooldown_max
        self.charge = None

        if not isinstance(cooldown_min, int) or not isinstance(cooldown_max, int):
            raise TypeError("Les cooldowns doivent être des entiers.")

        if cooldown_min < 0 or cooldown_max < 0:
            raise ValueError("Les cooldowns ne peuvent pas être négatifs.")

        if cooldown_min > cooldown_max:
            raise ValueError("Le cooldown minimum ne peut pas être supérieur au cooldown maximum.")

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

    def jouer_son(self):
        """Joue le son aléatoire comme attendu"""
        file_path = self.localise_son()
        # Initialiser Pygame est necessaire :pygame.mixer.init avant
        try:
            self.charge = pygame.mixer.Sound(file_path)
            t = random.randint(self.cooldown_min, self.cooldown_max) * 1000
            debut = pygame.time.get_ticks()  # l'heure de début
            running = True
            son_joue = False  # Indicateur pour savoir si le son a été joué

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    # temps écoulé
                    temps_ecoule = pygame.time.get_ticks() - debut
                    if temps_ecoule >= t and not son_joue:
                        self.charge.play()  # Jouer le son
                        son_joue = True  # Marquer le son comme joué
            t = (
                random.randint(self.cooldown_min, self.cooldown_max) + self.charge.get_length()
            ) * 1000
            debut = pygame.time.get_ticks()
        except pygame.error as e:
            print(f"Erreur lors de la lecture du fichier : {e}")

    def Arret_Son(self):
        if self.charge:
            self.charge.stop()
            self.charge = None
        else:
            print(f"le son {self.id_freesound} ne joue pas : pygame_error")
