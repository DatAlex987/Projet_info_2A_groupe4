import pygame
from os import getenv


class Son:
    """
    Classe représentant tous les sons qui ont été téléchargés afin d'être ajoutés à des scènes

    Attributs
    ----------
    nom : str
        nom
    description : str
        description
    duree : date
        duree initiale du son
    id_freesound : str
        identifiant du son sur l'API Freesound
    tags : list[str]
        mots clés permettant de qualifier le son

    Examples
    --------
    """

    def __init__(self, nom, description, duree, id_freesound, tags):
        """Constructeur"""
        self.nom = nom
        self.description = description
        self.duree = duree
        self.id_freesound = id_freesound
        self.tags = tags

        if not isinstance(id_freesound, str):
            raise TypeError("L'identifiant son doit être une instance de string.")

        # Initialisation de pygame et du mixer
        pygame.mixer.init()

    def charger_son(self) -> None:
        fichier_son = getenv("DOSSIER_SAUVEGARDE") + "/f'{self.id_freesound}.mp3'"
        # Charger le son
        pygame.mixer.music.load(fichier_son)

    def JouerSon(self) -> None:
        try:
            self.charger_son()
            # Jouer le son
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Erreur lors de la lecture du fichier son : {e}")

    def Arret_Son(self) -> None:
        pygame.mixer.music.stop()
