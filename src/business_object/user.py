import hashlib
from business_object.personne import Personne
import datetime
import re


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

    def __init__(self, nom, prenom, date_naissance, id_user, mdp, SD_possedes):
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
        """
        if not isinstance(nom, str):
            raise TypeError("Le nom doit être une instance de str.")
        if not isinstance(prenom, str):
            raise TypeError("Le prénom doit être une instance de str.")
        if not isinstance(date_naissance, datetime.date):
            raise TypeError("La date de naissance doit être une instance datetime.")
        if not isinstance(id_user, str):
            raise TypeError("Le nom d'utilisateur doit être une instance de str.")
        if not isinstance(mdp, str):
            raise TypeError("Le mot de passe doit être une instance de str.")
        if not isinstance(SD_possedes, list):
            raise TypeError("La liste des Sound-decks possédées doit être une instance de list.")
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

        super().__init__(nom, prenom, date_naissance)
        self.id_user = id_user
        self.mot_de_passe_hash = self._hash_mdp(mdp)
        self.SD_possedes = SD_possedes

    def _hash_mdp(self, mdp):
        mdp_combine = mdp + self.id_user
        return hashlib.pbkdf2_hmac(
            "sha256", mdp_combine.encode("utf-8"), self.nom.encode("utf-8"), 100000
        )

    def supprimer_utilisateur(self):
        self.id_user = None
        self.mot_de_passe_hash = None
        print("L'utilisateur a été supprimé avec succès.")
