"from user.py import User"


class Scene:
    """
    Classe représentant un scene : un groupement cohérent de son selon un lieu, une ambiance, etc...

    Attributs
    ----------
    nom : str
        nom
    description : str
        description
    id_scene : str
        identifiant de scene
    sons : list[str]
        liste des sons présents dans la scène
    auteur : User
        auteur de la scène
    date_creation

    Examples
    --------
    """

    def __init__(self, nom, description, id_scene, sons, auteur, date_creation):
        """Constructeur"""
        self.nom = nom
        self.description = description
        self.id_scene = id_scene
        self.sons = sons
        self.auteur = auteur
        self.date_creation = date_creation

        if not isinstance(id_scene, str):
            raise TypeError("L'identifiant scène doit être une instance de string.")
        if not isinstance(nom, str):
            raise TypeError("Le nom doit etre une instance de str")
        if not isinstance

    def modifier_nom_scene(self, nouveau_nom):
        """Modifier le nom de la scène"""
        self.nom = nouveau_nom

    def modifier_description_scene(self, nouvelle_description):
        """Modifier la description de la scène"""
        self.description = nouvelle_description


"bp de méthodes à ajouter"
