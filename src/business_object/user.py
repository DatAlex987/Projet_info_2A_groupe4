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
    pseudo : str
        Pseudonyme de l'utilisateur pour se connecter à l'application
    Méthodes
    --------
    supprimer_utilisateur() -> None:
        Supprime l'utilisateur en réinitialisant ses données.
    """

    def __init__(
        self, nom, prenom, date_naissance, id_user, mdp=None, SD_possedes=None, pseudo=None
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
        # Vérifications de type dans l'ordre spécifié par les tests
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

    def _hash_mdp(self, mdp):
        gen_hash = hashlib.pbkdf2_hmac(
            "sha256", mdp.encode("utf-8"), self.nom.encode("utf-8"), 100000
        )
        return gen_hash.hex()
        # Hash de type byte converti en hexadecimal. Evite les erreurs lors de l'authentification

    # SERT A RIEN

    def supprimer_utilisateur(self):
        self.id_user = None
        self.mot_de_passe_hash = None
        self.pseudo = None
        print("L'utilisateur a été supprimé avec succès.")
