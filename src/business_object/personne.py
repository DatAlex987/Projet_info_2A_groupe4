import datetime


class Personne:
    """
    Classe représentant tout personne pouvant utiliser l'application : un utilisateur (client) ou
    un administrateur

    Attributs
    ----------
    nom : str
        nom
    prenom : str
        prenom
    date_naissance : datetime.date
        date de naissance
    """

    def __init__(self, nom: str, prenom: str, date_naissance: datetime.date):
        """Constructeur"""
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance

    def modifier_nom_personne(self, nouveau_nom: str):
        """Modifier le nom de la personne"""
        if not isinstance(nouveau_nom, str):
            raise TypeError("Le nouveau nom doit être une instance de str.")
        self.nom = nouveau_nom

    def modifier_prenom_personne(self, nouveau_prenom: str):
        """Modifier le prénom de la personne"""
        if not isinstance(nouveau_prenom, str):
            raise TypeError("Le nouveau prenom doit être une instance de str.")
        self.prenom = nouveau_prenom
