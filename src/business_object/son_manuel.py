from business_object.son import Son
import pygame
import threading


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
        self.start_key: str = start_key
        self.charge = None
        if not isinstance(start_key, str):
            raise TypeError("la touche doit être de type String")

    def modifier_key(self, new_key):
        """Modifier la touche pour lancer un son"""
        self.start_key = new_key

    def Arret_Son(self):
        while self.charge:
            i = input(
                f"Appuyer sur m pour arreter le son manuel ou {self.start_key} pour le déclencher "
            )
            if i == "m":
                self.charge.stop()
                self.charge = None
            if i == f"{self.start_key}":
                self.charge.play()

    def jouer_son(self):
        """lance le son après déclenchement"""
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
