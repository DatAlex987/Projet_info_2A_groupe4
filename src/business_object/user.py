import os
import hashlib
from datetime import date


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
    Méthodes
    --------
    supprimer_utilisateur() -> None:
        Supprime l'utilisateur en réinitialisant ses données.
    """

<<<<<<< HEAD
    def __init__(self, nom, prenom, date_naissance, id_user, mdp):
=======
    def __init__(self, nom, prenom, date_naissance, id_user, mdp, SD_possedes):
>>>>>>> e3ea40b9629ee51f992e0d51e31d074b8744a9fd
        """
        Initialise un nouvel utilisateur avec les attributs de la classe Personne et ceux propre à un utilisateur.

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
        """
        super().__init__(nom, prenom, date_naissance)
        self.id_user = id_user
        self.mot_de_passe_hash = self._hash_mot_de_passe(mdp)
<<<<<<< HEAD
=======
        self.SD_possedes = SD_possedes
>>>>>>> e3ea40b9629ee51f992e0d51e31d074b8744a9fd

    def _hash_mdp(self, mdp):
        mdp_combine = mdp + self.id_user
        return hashlib.pbkdf2_hmac("sha256", mdp_combine.encode("utf-8"), os.urandom(16), 100000)

    def supprimer_utilisateur(self):
        self.id_user = None
        self.mot_de_passe_hash = None
        print("L'utilisateur a été supprimé avec succès.")
