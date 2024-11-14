from business_object.son import Son
import pygame


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

    def __init__(self, nom, description, duree, id_freesound, tags, start_key):
        super().__init__(nom, description, duree, id_freesound, tags)
        self.start_key: str = start_key
        self.charge = None
        if not isinstance(start_key, str):
            raise TypeError("la touche doit être de type String")

    def modifier_key(self, new_key):
        """Modifier la touche pour lancer un son"""
        self.start_key = new_key

    def jouer_son(self):
        """lance le son après déclenchement"""
        file_path = self.localise_son()
        # Initialiser Pygame est necessaire :pygame.mixer.init avant
        try:
            self.charge = pygame.mixer.Sound(file_path)
            print("chargé")
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if pygame.key.name(event.key) == self.start_key:
                            self.charge.play()
        except pygame.error as e:
            print(f"Erreur lors de la lecture du fichier : {e}")

    def Arret_Son(self):
        if self.charge:
            self.charge.stop()
            self.charge = None
        else:
            print(f"le son {self.id_freesound} ne joue pas : pygame_error")
