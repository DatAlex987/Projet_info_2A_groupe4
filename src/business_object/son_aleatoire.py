from business_object.son import Son
import pygame
import random
import threading


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

    def modifier_cooldown_min(self, new_cooldown_min):
        """Modifier les paramètres de cooldown d'un son aléatoire."""
        if not isinstance(new_cooldown_min, int):
            raise TypeError("Les cooldowns doivent être des entiers.")
        if new_cooldown_min < 0:
            raise ValueError("Les cooldowns ne peuvent pas être négatifs.")
        self.cooldown_min = new_cooldown_min

    def modifier_cooldown_max(self, new_cooldown_max):
        """Modifier les paramètres de cooldown d'un son aléatoire."""
        if not isinstance(new_cooldown_max, int):
            raise TypeError("Les cooldowns doivent être des entiers.")
        if new_cooldown_max < 0:
            raise ValueError("Les cooldowns ne peuvent pas être négatifs.")
        self.cooldown_max = new_cooldown_max

    def activ_son_alea(self, debut, t):
        t = (random.randint(self.cooldown_min, self.cooldown_max) + self.charge.get_length()) * 1000
        debut = pygame.time.get_ticks()
        return [debut, t]

    # Thread Worker qui exécute la fonction chaque fois que l'événement est déclenché
    def thread_worker(self, event, t, debut):
        while True:
            event.wait()  # Attendre que l'événement soit déclenché
            event.clear()  # Réinitialiser l'événement pour pouvoir attendre à nouveau
            temps_ecoule = pygame.time.get_ticks() - debut
            if temps_ecoule >= t:
                self.charge.play()  # Jouer le son

    def Arret_Son(self):
        if self.charge:
            input("Appuyer sur m pour arreter le son aleatoire")
            self.charge.stop()
            self.charge = None
        else:
            print(f"le son {self.id_freesound} ne joue pas : pygame_error")

    def jouer_son(self):
        """Joue le son aléatoire comme attendu"""
        file_path = self.localise_son()
        # Initialiser Pygame est necessaire :pygame.mixer.init avant
        try:
            self.charge = pygame.mixer.Sound(file_path)
            t = random.randint(self.cooldown_min, self.cooldown_max) * 1000
            debut = pygame.time.get_ticks()  # l'heure de début
            while self.charge:
                temps_ecoule = pygame.time.get_ticks() - debut
                if temps_ecoule >= t:
                    self.charge.play()  # Jouer le son

            thread_A = threading.Thread(target=self.Arret_Son)
            thread_A.daemon = True  # Ensure it exits when the main program does
            thread_A.start()
        except pygame.error as e:
            print(f"Erreur lors de la lecture du fichier : {e}")
