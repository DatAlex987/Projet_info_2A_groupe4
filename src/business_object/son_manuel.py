from business_object.son import Son
import re
import pygame


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

    def __init__(self, nom, description, duree, id_freesound, tags, start_key):
        super().__init__(nom, description, duree, id_freesound, tags)
        self.start_key: str = start_key

    def modifier_key(self, new_key):
        """Modifier la touche pour lancer un son"""
        self.start_key = new_key

    def get_pygame_key(self):
        return f"K_{self.start_key}"

    def jouer_son_manuel(self):
        """lance le son après déclenchement"""
        chaine = "K_" + self.start_key
        chaine_sans_guillemets = re.sub(r'"', "", chaine)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Vérifier si une touche du clavier est pressée
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.chaine_sans_guillemets:
                        self.JouerSon()
