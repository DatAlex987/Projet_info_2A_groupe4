import random
import time
import threading
import pygame

####
from business_object.son import Son


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

    def __init__(
        self, nom, description, duree, id_son, id_freesound, tags, cooldown_min, cooldown_max
    ):
        super().__init__(nom, description, duree, id_son, id_freesound, tags)
        """Constructeur"""
        self.cooldown_min = cooldown_min
        self.cooldown_max = cooldown_max
        self.charge = None
        self.thread = None
        self.event_son = None

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

    def Arret_Son(self):
        """Arrête la lecture du son."""
        self.en_jeu = False
        if self.thread and self.thread.is_alive():
            self.thread.join()  # Attendre que le thread se termine
        self.charge.stop()

    def jouer_Son(self):
        """Lance la boucle dans un thread séparé."""
        if not self.thread or not self.thread.is_alive():
            self.en_jeu = True
            self.thread = threading.Thread(target=self.boucle_son)
            self.thread.start()

    def boucle_son(self):
        """Méthode gérant les délais et le déclenchement des événements."""
        while self.en_jeu:
            delai = random.randint(self.cooldown_min, self.cooldown_max)
            time.sleep(delai)
            pygame.event.post(pygame.event.Event(self.event_son))  # Déclencher la lecture du son
            time.sleep(self.charge.get_length())  # Attendre la durée du son
            if not self.en_jeu:
                break
