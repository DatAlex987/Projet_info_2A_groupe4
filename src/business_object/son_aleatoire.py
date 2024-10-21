from src.business_object.son import Son


class Son_Aleatoire(Son):
    """
    Classe fille de son qui permet de jouer un son de manière aléatoire sur une plage définie

    Attributs
    ----------
    cooldown_min : int
        temps minimum avant que le son soit rejoué
    cooldown_max : int
        temps maximum avant que le son soit rejoué

    Examples
    --------
    """

    def __init__(self, nom, description, duree, id_freesound, tags, cooldown_min, cooldown_max):
        super().__init__(nom, description, duree, id_freesound, tags)
        self.cooldown_min = cooldown_min
        self.cooldown_max = cooldown_max

    def modifier_cooldown(self, new_cooldown_min, new_cooldown_max):
        """Modifier les paramètres de cooldown d'un son aléatoire"""
        self.cooldown_min = new_cooldown_min
        self.cooldown_max = new_cooldown_max
