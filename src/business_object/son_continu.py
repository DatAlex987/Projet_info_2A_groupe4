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
        pygame.mixer.music.unload()

    def jouer_Son(self):
        fp = self.localise_son()
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()
