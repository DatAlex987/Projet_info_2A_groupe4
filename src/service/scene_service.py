from utils.log_decorator import log
from business_object.scene import Scene
from view.session import Session
from dao.scene_dao import SceneDAO


class SceneService:
    """Méthodes de service des scènes"""

    def formatage_question_scenes_of_sd(self, id_sd: str):
        sds_user = Session().utilisateur.SD_possedes
        for sd in sds_user:
            if sd.id_sd == id_sd:
                sd_selectionne = sd
        choix = []
        compteur = 1
        for scene in sd_selectionne.scenes:
            mise_en_page_ligne = (
                f"{compteur}. {scene.id_scene} | {scene.nom} | {scene.date_creation}"
            )
            choix.append(mise_en_page_ligne)
            compteur += 1
        choix.append("Ajouter une scène")
        choix.append("Supprimer une scène")
        choix.append("Supprimer la sound-deck")
        choix.append("Retour au menu de paramétrage")
        return choix


"""
    @log
    def creer(**kwargs):
        "Création d'une scène à partir de ses attributs"
        new_scene = Scene(**kwargs)
        return new_scene if SceneDAO().ajouter_scene(new_scene) else None

    @log
    def supprimer(self, scene) -> bool:
        "Supprimme une scene"
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
"""
