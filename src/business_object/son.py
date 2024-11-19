import datetime
import os
import pygame
import threading
from dotenv import load_dotenv
from abc import ABC, abstractmethod

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"


class Son(ABC):
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

    def __init__(self, nom, description, duree, id_son, id_freesound, tags):
        """Constructeur"""
        self.nom = nom
        self.description = description
        self.duree = duree
        self.id_freesound = id_freesound
        self.id_son = id_son
        self.tags = tags
        self.charge = None
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
        if not isinstance(id_son, str):
            raise TypeError("L'identifiant unique du son doit être une instance de string.")

    def localise_son(self):
        """localise un son à l'aide des variables d'environnement"""
        load_dotenv()
        directory = os.getenv("DOSSIER_SAUVEGARDE")
        matching_files = []
        for filename in os.listdir(directory):
            if self.id_freesound in filename:
                matching_files.append(filename)
        file_path = os.path.join(directory, f"{matching_files[0]}")
        if not os.path.exists(file_path):
            print(f"Erreur : Le fichier {file_path} n'existe pas.")
        else:
            print(f"fichier {file_path} trouvé")
        return file_path

    def jouer_son_preview(self):
        file_path = self.localise_son()
        try:
            # faire le pygame.mixer.init() avant
            pygame.mixer.music.load(file_path)
            print("load")
            pygame.mixer.music.play()
            print("jeu")
            # Run the input listener in a separate thread
            thread = threading.Thread(target=self.Arret_Son)
            # thread.daemon = True  # Ensure it exits when the main program does
            thread.start()
        except pygame.error as e:
            print(f"Erreur lors de la lecture du fichier : {e}")

    @abstractmethod
    def Arret_Son(self) -> None:
        pass

    @abstractmethod
    def jouer_Son(self) -> None:
        pass

    def modifier_nom(self, new_nom: str):
        self.nom = new_nom

    def modifier_description(self, new_desc: str):
        self.description = new_desc
