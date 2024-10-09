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
    date_naissance : date
        date de naissance

    Examples
    --------
    >>> personne = Personne("Bocquet", "Noémie", "2003-08-08")
    >>> personne.modifier_prenom("Théo")
    >>> print(personne.prenom)
    Théo

    """

    def __init__(self, nom, prenom, date_naissance):
        """Constructeur"""
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance

    def modifier_nom(self, nouveau_nom):
        """Modifier le nom de la personne"""
        self.nom = nouveau_nom

    def modifier_prenom(self, nouveau_prenom):
        """Modifier le prénom de la personne"""
        self.prenom = nouveau_prenom


if __name__ == "__main__":
    import doctest

    doctest.testmod()
