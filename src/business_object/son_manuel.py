from business_object.son import Son
import pygame
<<<<<<< HEAD
import threading
=======
>>>>>>> 9f491eb676a209b5d458bbb46088134d24434e81


class Son_Manuel(Son):
    """
    Classe fille de son qui permet de jouer un son quand on le souhaite à partir d'une touche du
    clavier bien définie


    Attributs
    ----------
    start_key : str
        touche pour lancer le lon

    Examples
    --------
    """

    def __init__(self, nom, description, duree, id_son, id_freesound, tags, start_key):
        super().__init__(nom, description, duree, id_son, id_freesound, tags)
        self.start_key: str = start_key  # La touche pour lancer le son
        self.charge = None  # Instance attribute for sound
        # THEO FROM HERE
        self.sound_playing = False  # To track if the sound is playing
        self.key_thread = None  # To store the thread for key listening

        # Key mapping for numeric keypad
        key_mapping = {
            "0": pygame.K_KP_0,
            "1": pygame.K_KP_1,
            "2": pygame.K_KP_2,
            "3": pygame.K_KP_3,
            "4": pygame.K_KP_4,
            "5": pygame.K_KP_5,
            "6": pygame.K_KP_6,
            "7": pygame.K_KP_7,
            "8": pygame.K_KP_8,
            "9": pygame.K_KP_9,
        }
        self.pygame_keycode = key_mapping.get(start_key)

        if not isinstance(start_key, str):
            raise TypeError("la touche doit être de type String")

    def modifier_key(self, new_key):
        """Modifier la touche pour lancer un son"""
        self.start_key = new_key

    def Arret_Son(self):
        self.charge.stop()
        self.charge = None

    def jouer_Son(self):
        if self.charge is not None:
            self.charge.play()
            self.charge.set_volume(0.6)

    def convert_to_kpg(self, char):
        """
        Convertit un caractère en clé Pygame associée.

        :param char: Une chaîne de caractères (exemple : "f").
        :return: La constante Pygame associée (exemple : pygame.K_f).
        :raises ValueError: Si le caractère n'est pas valide ou n'a pas de clé associée.
        """

        # Vérification que la chaîne est une lettre ou un chiffre
        if len(char) != 1:
            raise ValueError("Veuillez entrer un seul caractère.")

        # Convertir la lettre en constante Pygame
        key = getattr(pygame, f"K_{char}", None)
        if key is None:
            raise ValueError(f"Aucune clé Pygame trouvée pour '{char}'.")

        return key

    """
    def Arret_Son(self):
        if self.charge:
            i = input(
                f"Appuyer sur m pour arreter le son manuel ou {self.start_key} pour le déclencher "
            )
            if i == "m":
                self.charge.stop()
                self.charge = None
            if i == f"{self.start_key}":
                self.charge.play()

    def jouer_son(self):
        file_path = self.localise_son()
        # Initialiser Pygame est necessaire :pygame.mixer.init avant
        try:
            self.charge = pygame.mixer.Sound(file_path)
            print("chargé")
            while self.charge:
                thread_A = threading.Thread(target=self.Arret_Son)
                thread_A.daemon = True
                thread_A.start()
        except pygame.error as e:
            print(f"Erreur lors de la lecture du fichier : {e}")
    """
