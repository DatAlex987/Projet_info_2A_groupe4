import pygame
import datetime

####
from business_object.son import Son


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

    def __init__(
        self,
        nom: str,
        description: str,
        duree: datetime.timedelta,
        id_son: str,
        id_freesound: str,
        tags: list,
        start_key: str,
    ):
        super().__init__(nom, description, duree, id_son, id_freesound, tags)
        self.start_key: str = start_key  # La touche pour lancer le son
        self.charge = None  # Instance attribute for sound

        if not isinstance(start_key, str):
            raise TypeError("la touche doit être de type String")

    def modifier_key(self, new_key: str):
        """Modifier la touche pour lancer un son"""
        self.start_key = new_key

    def Arret_Son(self):
        self.charge.stop()
        self.charge = None

    def jouer_Son(self):
        if self.charge is not None:
            self.charge.play()
            self.charge.set_volume(0.6)

    def convert_to_kpg(self, char: str):
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
