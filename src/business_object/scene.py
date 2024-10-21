from business_object.son import Son
from business_object.son_aleatoire import Son_aleatoire
from business_object.son_continu import Son_Continu
from business_object.son_manuel import Son_Manuel


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
    sons_aleatoires : list[Son_Aleatoire]
        liste des sons aléatoires présents dans la scène
    sons_continus : list[Son_Continu]
        liste des sons continus présents dans la scène
    sons_manuels : list[Son_Manuel]
        liste des sons manuels présents dans la scène
    auteur : User
        auteur de la scène
    date_creation
    """

    def __init__(
        self,
        nom,
        description,
        id_scene,
        sons_aleatoires,
        sons_manuels,
        sons_continus,
        auteur,
        date_creation,
    ):
        """Constructeur"""
        self.nom = nom
        self.description = description
        self.id_scene = id_scene
        self.sons_aleatoires = sons_aleatoires
        self.sons_manuels = sons_manuels
        self.sons_continus = sons_continus
        self.auteur = auteur
        self.date_creation = date_creation

        if not isinstance(id_scene, str):
            raise TypeError("L'identifiant scène doit être une instance de string.")
        if not isinstance(nom, str):
            raise TypeError("Le nom doit etre une instance de str")

    def modifier_nom(self, nouveau_nom):
        """Modifier le nom de la scène"""
        self.nom = nouveau_nom

    def modifier_description(self, nouvelle_description):
        """Modifier la description de la scène"""
        self.description = nouvelle_description

    def ajouter_son_aleatoire(self, nouveau_son_aleatoire):
        """Ajoute un nouveau son aléatoire dans la scène"""
        self.sons_aleatoires.append(nouveau_son_aleatoire)

    def ajouter_son_continu(self, nouveau_son_continu):
        """Ajoute un nouveau son continu dans la scène"""
        self.sons_continus.append(nouveau_son_continu)

    def ajouter_son_manuel(self, nouveau_son_manuel):
        """Ajoute un nouveau son manuel dans la scène"""
        self.sons_manuels.append(nouveau_son_manuel)

    def supprimer_scene(self):
        del self
