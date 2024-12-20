import datetime
import re
import hashlib

####
from business_object.personne import Personne
from business_object.sd import SD
from business_object.scene import Scene
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_manuel import Son_Manuel
from business_object.son_continu import Son_Continu


class User(Personne):
    """
    Classe représentant un utilisateur de l'application.

    Hérite de la classe Personne.

    Attributs
    ----------
    id_user : str
        Nom d'utilisateur unique et obligatoire pour se connecter à l'application.
    mot_de_passe_hash : str
        Hachage du mot de passe de l'utilisateur combiné avec un élément lié à l'utilisateur.
    SD_possedes : list[SD]
        Liste des Sound-decks possédées par l'utilisateur.
    pseudo : str
        Pseudonyme de l'utilisateur pour se connecter à l'application
    Méthodes
    --------
    supprimer_utilisateur() -> None:
        Supprime l'utilisateur en réinitialisant ses données.
    """

    def __init__(
        self,
        nom: str,
        prenom: str,
        date_naissance: datetime.date,
        id_user: str,
        mdp=None,
        SD_possedes=None,
        pseudo=None,
    ):
        # mdp optionel. N'est précisé que lors de la première instantiation
        # (pour éviter de hasher le mdp déjà hashé lors de l'instantiation après
        # requête dans la bdd par exemple)
        """
        Initialise un nouvel utilisateur avec les attributs de la classe
        Personne et ceux propre à un utilisateur.

        Parameters
        ----------
        nom : str
            Nom de famille de l'utilisateur.
        prenom : str
            Prénom de l'utilisateur.
        date_naissance : date
            Date de naissance de l'utilisateur (au format 'YYYY-MM-DD').
        id_user : str
            Nom d'utilisateur pour la connexion.
        mdp : str
            Mot de passe en clair à hacher.
        pseudo : str
            Pseudonyme de l'utilisateur pour se connecter à l'application
        """
        # Vérifications de type
        if not isinstance(nom, str):
            raise TypeError("Le nom doit être une instance de str.")
        if not isinstance(prenom, str):
            raise TypeError("Le prénom doit être une instance de str.")
        if not isinstance(date_naissance, datetime.date):
            raise TypeError("La date de naissance doit être une instance datetime.")
        if not isinstance(id_user, str):
            raise TypeError("L'identifiant de l'utilisateur doit être une instance de str.")
        if mdp is not None:
            # Pour traiter le cas discuté plus haut, un mot de passe est désormais facultatif
            # Néanmoins, chaque instance de User utilisée pour ajouter un user dans la bdd
            # devra comporter un mot de passe (pour s'assurer qu'un user a bel et bien un mdp).
            if not isinstance(mdp, str):
                raise TypeError("Le mot de passe doit être une instance de str.")
            if len(mdp) < 8:
                raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")
            if not re.search(r"[A-Z]", mdp):
                raise ValueError("Le mot de passe doit contenir au moins une lettre majuscule.")
            if not re.search(r"[a-z]", mdp):
                raise ValueError("Le mot de passe doit contenir au moins une lettre minuscule.")
            if not re.search(r"[0-9]", mdp):
                raise ValueError("Le mot de passe doit contenir au moins un chiffre.")
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", mdp):
                raise ValueError("Le mot de passe doit contenir au moins un caractère spécial.")
        if SD_possedes is not None:
            if not isinstance(SD_possedes, list):
                raise TypeError(
                    "La liste des Sound-decks possédées doit être une instance de list."
                )
        if not isinstance(pseudo, str):
            raise TypeError("Le pseudo de l'utilisateur doit être une instance de str.")

        super().__init__(nom, prenom, date_naissance)
        self.id_user = id_user
        self.mot_de_passe_hash = self._hash_mdp(mdp) if mdp else None
        self.SD_possedes = SD_possedes
        self.pseudo = pseudo

    def _hash_mdp(self, mdp: str):
        gen_hash = hashlib.pbkdf2_hmac(
            "sha256", mdp.encode("utf-8"), self.nom.encode("utf-8"), 100000
        )
        return gen_hash.hex()
        # Hash de type byte converti en hexadecimal. Evite les erreurs lors de l'authentification

    def ajouter_sd(self, sd: SD):
        self.SD_possedes.append(sd)

    def enlever_sd(self, sd: SD):
        for sd_pos in self.SD_possedes:
            if sd.id_sd == sd_pos.id_sd:
                self.SD_possedes.remove(sd_pos)

    def ajouter_scene_a_sd(self, id_sd: str, scene: Scene):
        for sd in self.SD_possedes:
            if sd.id_sd == id_sd:
                sd.scenes.append(scene)

    def supprimer_scene_a_sd(self, id_sd: str, id_scene: str):
        for sd in self.SD_possedes:
            if sd.id_sd == id_sd:
                for scene in sd.scenes:
                    if scene.id_scene == id_scene:
                        sd.scenes.remove(scene)

    def ajouter_son_a_scene(self, id_sd: str, id_scene: str, son):
        for sd in self.SD_possedes:
            if sd.id_sd == id_sd:
                for scene in sd.scenes:
                    if scene.id_scene == id_scene:
                        if isinstance(son, Son_Aleatoire):
                            scene.ajouter_son_aleatoire(nouveau_son_aleatoire=son)
                        elif isinstance(son, Son_Manuel):
                            scene.ajouter_son_manuel(nouveau_son_manuel=son)
                        elif isinstance(son, Son_Continu):
                            scene.ajouter_son_continu(nouveau_son_continu=son)

    def supprimer_son_a_scene(self, id_sd: str, id_scene: str, son):
        for sd in self.SD_possedes:
            if sd.id_sd == id_sd:
                for scene in sd.scenes:
                    if scene.id_scene == id_scene:
                        if isinstance(son, Son_Aleatoire):
                            for son_alea in scene.sons_aleatoires:
                                if son_alea.id_son == son.id_son:
                                    scene.supprimer_son_aleatoire(son_aleatoire=son_alea)
                        elif isinstance(son, Son_Manuel):
                            for son_manuel in scene.sons_manuels:
                                if son_manuel.id_son == son.id_son:
                                    scene.supprimer_son_manuel(son_manuel=son_manuel)
                        elif isinstance(son, Son_Continu):
                            for son_cont in scene.sons_continus:
                                if son_cont.id_son == son.id_son:
                                    scene.supprimer_son_continu(son_continu=son_cont)
