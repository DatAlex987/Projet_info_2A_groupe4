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

    def __init__(self, nom, description, duree, id_freesound, tags):
        super().__init__(nom, description, duree, id_freesound, tags)
        self.lp = -1

    def jouer_son(self):
        file_path = self.localise_son()
        try:
            # faire le pygame.mixer.init() avant
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play(loops=self.lp)
        except pygame.error as e:
            print(f"Erreur lors de la lecture du fichier : {e}")

    def Arret_Son(self):
        pygame.mixer.music.stop()
