import datetime
import pygame
import os
from dotenv import load_dotenv
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"


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

    def Arret_Son(self) -> None:
        if self.charge:
            self.charge.stop()
            self.charge = None
        else:
            print(f"le son {self.id_freesound} ne joue pas : pygame_error")

    def JouerSon(self) -> None:
        """Méthode globale pour charger puis jouer un son avec Pygame"""
        load_dotenv()
        directory = os.getenv("DOSSIER_SAUVEGARDE")
        file_path = os.path.join(directory, f"son_{self.id_freesound}.mp3")
        if not os.path.exists(file_path):
            print(f"Erreur : Le fichier {file_path} n'existe pas.")
        else:
        
        # Initialiser Pygame est necessaire :pygame.mixer.init()
        
            try:
                self.charge = pygame.mixer.Sound(file_path)
                self.charge.play()
                
                start_time = pygame.time.get_ticks()
            
                while pygame.mixer.get_busy():
                    current_time = pygame.time.get_ticks()
                    if (current_time - start_time) > 30000:  # 30 000 ms = 30 secondes
                        self.Arret_Son()

            except pygame.error as e:
                print(f"Erreur lors de la lecture du fichier : {e}")
        """
        try:
            expected_path = os.getenv("DOSSIER_SAUVEGARDE")
            if expected_path is None:
                raise ValueError("Le chemin attendu (expected_path) ne doit pas être None.")
            else:
                fichier_son = os.path.normpath(
                    os.path.join(expected_path, f"{self.id_freesound}.mp3")
                )
                # Charger le son
                self.charge = pygame.mixer.Sound(fichier_son)
                # Jouer le son
                (self.charge).play(loops=self.lp)
        except pygame.error as e:
            print(f"Erreur lors de la lecture du fichier son : {e}")
        except FileNotFoundError:
            print(rf"Le fichier son {fichier_son} n'a pas été trouvé.")"""

    
