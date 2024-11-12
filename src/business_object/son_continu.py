from business_object.son import Son


class Son_Continu(Son):
    """
    Classe fille de son qui permet de jouer un son en continu durant une scène


    Attributs
    ----------
    Examples
    --------
    """

    def __init__(self, nom, description, duree, id_freesound, tags):
        super().__init__(nom, description, duree, id_freesound, tags)
        self.lp = -1

    def jouer_son_en_boucle(self):
        """Lancer le son en boucle"""
        self.jouer_son()
