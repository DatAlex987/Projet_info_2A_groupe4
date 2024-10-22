from business_object.scene import Scene
from business_object.user import User
import datetime


class SD:
    """
    Classe représentant un sound-deck : un groupement de scènes formant une partie de jeu de rôle

    Attributs
    ----------
    nom : str
        nom
    description : str
        description
    id_sd : int
        identifiant de sound-deck
    scenes : list[Scene]
        liste des scènes présentes dans la sound-deck
    date_creation : date
        date de création du sound-deck

    Examples
    --------
    """

    def __init__(self, nom, description, id_sd, scenes, date_creation):
        "self.scenes à modifier dès que possible"
        """Constructeur"""
        self.nom = nom
        self.description = description
        self.id_sd = id_sd
        self.scenes = scenes
        self.date_creation = date_creation

        if not isinstance(id_sd, int):
            raise TypeError("L'identifiant sound-deck doit être un entier.")
        if not isinstance(nom, str):
            raise TypeError("Le nom doit etre une instance de str.")
        if not isinstance(description, str):
            raise TypeError("La description doit etre une instance de str.")
        if not isinstance(scenes, list):
            raise TypeError("Scènes doit etre une liste de scènes.")
        if not all(isinstance(element, Scene) for element in list):
            raise TypeError("Les éléments de la liste doivent etre des scènes.")
        if not isinstance(date_creation, datetime):
            raise TypeError("La date de creation doit etre une date.")

    def modifier_nom_sd(self, nouveau_nom):
        """Modifier le nom du sound-deck"""
        if not isinstance(nouveau_nom, str):
            raise TypeError("Le nouveau nom doit etre une instance de str.")
        self.nom = nouveau_nom


    def modifier_description_sd(self, nouvelle_description):
        """Modifier la description du sound-deck"""
         if not isinstance(nouvelle_description, str):
            raise TypeError("La nouvelle description doit etre une instance de str.")
        self.description = nouvelle_description


    def ajouter_scene(self, nouvelle_scene):
        """ajoute une scène au sound-deck"""
        if not isinstance(nouvelle_scene, Scene):
            raise TypeError ("La nouvelle scène doit etre une instance de Scene.")
        self.scenes.append(nouvelle_scene)

    def retirer_scene(self, scene):
        """retire une scène du sound-deck"""
        if scene in self.scenes:
            self.scenes.remove(scene)
        else:
            print(f"La scène '{scene}' n'existe pas dans la liste.")
