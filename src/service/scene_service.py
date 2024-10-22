from tabulate import tabulate

from utils.log_decorator import log
from utils.securite import hash_password

from business_object.scene import Scene
from dao.scene_dao import SceneDAO


class SceneService:
    """Méthodes des scènes"""

    @log
    def creer(**kwargs):
        """Création d'une scène à partir de ses attributs"""
        new_scene = Scene(**kwargs)
        return new_scene if SceneDAO().ajouter_scene(new_scene) else None

    @log
    def supprimer(self, scene) -> bool:
        """Supprimme une scene"""
        return SceneDAO().supprimer(scene)

    @log
    def modifier_nom(self, scene, new_name):
        pass

    @log
    def modifier_description(self, scene, new_desc):
        pass

    @log
    def ajouter_son_aleatoire(self, scene, new_son_aleatoire):
        pass

    @log
    def ajouter_son_manuel(self, scene, new_son_manuel):
        pass

    @log
    def ajouter_son_continu(self, scene, new_son_continu):
        pass

    @log
    def modifier_son_aleatoire(self, scene, new_son_aleatoire):
        pass

    @log
    def modifier_son_manuel(self, scene, new_son_manuel):
        pass

    @log
    def modifier_son_continu(self, scene, new_son_continu):
        pass
