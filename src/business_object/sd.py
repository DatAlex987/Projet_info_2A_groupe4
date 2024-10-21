"from scene.py import Scene"


class SD:
    """
    Classe représentant un sound-deck : un groupement de scènes formant une partie de jeu de rôle

    Attributs
    ----------
    nom : str
        nom
    description : str
        description
    id_sd : str
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

        if not isinstance(id_sd, str):
            raise TypeError("L'identifiant sound-deck doit être une instance de string.")

    def modifier_nom_sd(self, nouveau_nom):
        """Modifier le nom du sound-deck"""
        self.nom = nouveau_nom

    def modifier_description_sd(self, nouvelle_description):
        """Modifier la description du sound-deck"""
        self.description = nouvelle_description
