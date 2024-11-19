from business_object.son import Son
import random
import time


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
        self.charge.stop()
        self.charge = None

    def jouer_Son(self):
        dernier_temps = time.time()
        longueur = self.charge.get_lenght()
        c = 0
        while self.charge is not None:
            temps_actuel = time.time()
            t = random.randint(self.cooldown_min, self.cooldown_max)
            if temps_actuel - dernier_temps > t + (longueur) * c:
                self.charge.play()
                dernier_temps = temps_actuel
                if c == 0:
                    c += 1

    """
    def Arret_Son(self):
        if self.charge:
            input("Appuyer sur Entrée pour arreter le son aleatoire")
            self.charge.stop()
            self.charge = None

    def jouer_son(self):
        file_path = self.localise_son()
        # Initialiser Pygame est necessaire :pygame.mixer.init avant
        try:
            self.charge = pygame.mixer.Sound(file_path)
            t = random.randint(self.cooldown_min, self.cooldown_max)
            longueur = self.charge.get_length() // 1000
            time.sleep(t)
            self.charge.play()  # Jouer le son
            t = random.randint(self.cooldown_min, self.cooldown_max) + longueur
            debut = pygame.time.get_ticks()
            thread_A = threading.Thread(target=self.Arret_Son)
            thread_A.daemon = True  # Ensure it exits when the main program does
            thread_A.start()
            while self.charge:
                temps_ecoule = pygame.time.get_ticks() - debut
                if (temps_ecoule // 1000) >= t:
                    self.charge.play()  # Jouer le son
                    t = longueur + (random.randint(self.cooldown_min, self.cooldown_max))
                    debut = pygame.time.get_ticks()

        except pygame.error as e:
            print(f"Erreur lors de la lecture du fichier : {e}")

    def start_random_play(self):  # TEST THEO
        "Start random playback."

        def play_randomly():
            while self.charge is not None:
                self.charge.play()
                cooldown = random.randint(self.cooldown_min, self.cooldown_max)
                time.sleep(cooldown)

        if self.charge is None:
            self.play_sound()
            self.charge = threading.Thread(target=play_randomly, daemon=True)
            self.charge.start()
        else:
            self.stop_sound()
