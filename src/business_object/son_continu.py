from business_object.son import Son
import pygame


class Son_Continu(Son):
    """
    Classe fille de son qui permet de jouer un son en continu durant une scène


    Attributs
    ----------
    Examples
    --------
    """

    def __init__(self, nom, description, duree, id_son, id_freesound, tags):
        super().__init__(nom, description, duree, id_son, id_freesound, tags)

    def Arret_Son(self):
        pass

    def jouer_Son(self):
        if self.charge is not None:
            self.charge.play(loops=-1)

    """
    def Arret_Son(self):
        input("Appuyer sur Entrée pour arrêter le son")
        pygame.mixer.music.stop()

    def jouer_son(self):
        file_path = self.localise_son()
        try:
            # faire le pygame.mixer.init() avant
            pygame.mixer.music.load(file_path)
            print("load")
            pygame.mixer.music.play(loops=-1)
            print("jeu")
            # Run the input listener in a separate thread
            thread = threading.Thread(target=self.Arret_Son)
            # thread.daemon = True  # Ensure it exits when the main program does
            thread.start()
        except pygame.error as e:
            print(f"Erreur lors de la lecture du fichier : {e}")
    """
