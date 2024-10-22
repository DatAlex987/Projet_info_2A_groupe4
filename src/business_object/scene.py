from business_object.son import Son
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_continu import Son_Continu
from business_object.son_manuel import Son_Manuel
from business_object.user import User
import datetime


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

        if not isinstance(nom, str):
            raise TypeError("Le nom doit etre une instance de str.")
        if not isinstance(description, str):
            raise TypeError("La description doit être une instance de str.")
        if not isinstance(id_scene, str):
            raise TypeError("L'identifiant scène doit être une instance de string.")
        if not isinstance(sons_aleatoires, list):
            raise TypeError("La liste des sons aléatoires doit être une instance de list.")
        if not isinstance(sons_continus, list):
            raise TypeError("La liste des sons continus doit être une instance de list.")
        if not isinstance(sons_manuels, list):
            raise TypeError("La liste des sons manuels doit être une instance de list.")
        if not isinstance(auteur, User):
            raise TypeError("L'auteur doit être une instance de User.")
        if not isinstance(date_creation, datetime.date):
            raise TypeError("La date de création doit être une instance de str ou datetime.")

    def modifier_nom(self, nouveau_nom):
        """Modifier le nom de la scène"""
        if not isinstance(nouveau_nom, str):
            raise TypeError("Le nouveau nom doit etre une instance de str.")
        self.nom = nouveau_nom

    def modifier_description(self, nouvelle_description):
        """Modifier la description de la scène"""
        if not isinstance(nouvelle_description, str):
            raise TypeError("La nouvelle description doit etre une instance de str.")
        self.description = nouvelle_description

    def ajouter_son_aleatoire(self, nouveau_son_aleatoire):
        """Ajoute un nouveau son aléatoire dans la scène"""
        if not isinstance(nouveau_son_aleatoire, Son_Aleatoire):
            raise TypeError("Le nouveau son doit etre une instance de son aléatoire.")
        self.sons_aleatoires.append(nouveau_son_aleatoire)

    def ajouter_son_continu(self, nouveau_son_continu):
        """Ajoute un nouveau son continu dans la scène"""
        if not isinstance(nouveau_son_continu, Son_Continu):
            raise TypeError("Le nouveau son doit etre une instance de son continu.")
        self.sons_continus.append(nouveau_son_continu)

    def ajouter_son_manuel(self, nouveau_son_manuel):
        """Ajoute un nouveau son manuel dans la scène"""
        if not isinstance(nouveau_son_manuel, Son_Manuel):
            raise TypeError("Le nouveau son doit etre une instance de son manuel.")
        self.sons_manuels.append(nouveau_son_manuel)

    def supprimer_son_aleatoire(self, son_aleatoire):
        """Ajoute un nouveau son aléatoire dans la scène"""
        self.sons_aleatoires.remove(son_aleatoire)

    def supprimer_son_continu(self, son_continu):
        """Ajoute un nouveau son continu dans la scène"""
        self.sons_continus.remove(son_continu)

    def supprimer_son_manuel(self, son_manuel):
        """Ajoute un nouveau son manuel dans la scène"""
        self.sons_manuels.remove(son_manuel)

    def supprimer_scene(self):
        del self
