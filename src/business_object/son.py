import datetime
import pygame
import os


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
    son = Son(
        nom="The Imperial March",
        description="Luke, I am your father",
        duree=datetime.timedelta(seconds=45),
        id_freesound="039450",
        tags=["starwars", "Vador", "JW"]
    )
    """

    def __init__(self, nom, description, duree, id_freesound, tags):
        """Constructeur"""
        self.nom = nom
        self.description = description
        self.duree = duree
        self.id_freesound = id_freesound
        self.tags = tags
        self.charge = None
        self.lp = 0

        if not isinstance(nom, str):
            raise TypeError("Le nom doit etre une instance de str.")
        if not isinstance(description, str):
            raise TypeError("La description doit etre une instance de str.")
        if not isinstance(tags, list):
            raise TypeError("tags doit etre une liste de scènes.")
        if not all(isinstance(t, str) for t in tags):
            raise TypeError("Les éléments de la liste des tags doivent etre des scènes.")
        if not isinstance(duree, datetime.timedelta):
            raise TypeError("La durée doit etre une durée format datetime.timedelta.")
        if not isinstance(id_freesound, str):
            raise TypeError("L'identifiant freesound du son doit être une instance de string.")

    def JouerSon(self) -> None:
        """Méthode globale pour charger puis jouer un son avec Pygame"""
        try:
            expected_path = os.getenv("DOSSIER_SAUVEGARDE")
            fichier_son = os.path.normpath(os.path.join(expected_path, f"{self.id_freesound}.mp3"))
            # Charger le son
            self.charge = pygame.mixer.Sound(fichier_son)
            # Jouer le son
            (self.charge).play(loop=self.lp)
        except pygame.error as e:
            print(f"Erreur lors de la lecture du fichier son : {e}")
        except FileNotFoundError:
            print(rf"Le fichier son {fichier_son} n'a pas été trouvé.")

    def Arret_Son(self) -> None:
        (self.charge).stop()
        self.charge = None
