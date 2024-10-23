from utils.singleton import Singleton
from dao.db_connection import DBConnection
from business_object.sd import SD


class SDDAO(metaclass=Singleton):
    """Implémente les méthodes du CRUD pour accéder à la base de données des sound-decks"""

    def ajouter_sd(self, sd: SD) -> SD:
        """
        Ajoute un nouveau sound-deck à la base de données.

        Parameters
        ----------
        sd : SD
            L'objet SD à ajouter.

        Returns
        -------
        SD
            L'objet SD avec son ID mis à jour, ou None en cas d'échec.
        """
        if not self.valider_sd(sd):
            print("Données invalides fournies pour l'ajout du sound-deck.")
            return None

        try:
            with DBConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO ProjetInfo.SoundDeck(nom, description, date_creation)
                        VALUES (%(nom)s, %(description)s, %(date_creation)s)
                        RETURNING id_sd;
                        """,
                        {
                            "nom": sd.nom,
                            "description": sd.description,
                            "date_creation": sd.date_creation,
                        },
                    )
                    sd.id_sd = cursor.fetchone()["id_sd"]
            return sd
        except Exception as e:
            print(f"Erreur lors de l'ajout du sound-deck : {e}")
            return None

    def modifier_sd(self, sd: SD) -> SD:
        """
        Modifie les informations d'un sound-deck existant.

        Parameters
        ----------
        sd : SD
            L'objet SD avec les nouvelles informations.

        Returns
        -------
        SD
            L'objet SD avec les informations mises à jour, ou None en cas d'échec.
        """
        if not self.valider_sd(sd):
            print("Données invalides fournies pour la modification du sound-deck.")
            return None

        try:
            with DBConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE ProjetInfo.SoundDeck
                        SET nom = %(nom)s, description = %(description)s,
                        date_creation = %(date_creation)s
                        WHERE id_sd = %(id_sd)s;
                        """,
                        {
                            "nom": sd.nom,
                            "description": sd.description,
                            "date_creation": sd.date_creation,
                            "id_sd": sd.id_sd,
                        },
                    )
            return sd
        except Exception as e:
            print(f"Erreur lors de la modification du sound-deck avec ID {sd.id_sd} : {e}")
            return None

    def supprimer_sd(self, id_sd: int) -> bool:
        """
        Supprime un sound-deck par son ID.

        Parameters
        ----------
        id_sd : int
            L'ID du sound-deck à supprimer.

        Returns
        -------
        bool
            True si la suppression a réussi, sinon False.
        """
        if id_sd is None:
            print("ID sound-deck invalide fourni pour la suppression.")
            return False

        try:
            with DBConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM ProjetInfo.SoundDeck
                        WHERE id_sd = %(id_sd)s;
                        """,
                        {"id_sd": id_sd},
                    )
                    return cursor.rowcount > 0
        except Exception as e:
            print(f"Erreur lors de la suppression du sound-deck avec ID {id_sd} : {e}")
            return False

    def consulter_sds(self) -> list:
        """
        Récupère la liste de tous les sound-decks dans la base de données.

        Returns
        -------
        list
            Une liste d'objets SD contenant les informations des sound-decks.
        """
        try:
            with DBConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_sd, nom, description, date_creation
                        FROM ProjetInfo.SoundDeck;
                        """
                    )
                    res = cursor.fetchall()

                    if not res:
                        return []

                    return [
                        SD(
                            id_sd=row["id_sd"],
                            nom=row["nom"],
                            description=row["description"],
                            date_creation=row["date_creation"],
                        )
                        for row in res
                    ]
        except Exception as e:
            print(f"Erreur lors de la récupération des sound-decks : {e}")
            return []

    def rechercher_par_id_sd(self, id_sd: int) -> SD:
        """
        Recherche un sound-deck dans la base de données par son ID.

        Parameters
        ----------
        id_sd : int
            L'ID du sound-deck à rechercher.

        Returns
        -------
        SD
            Un objet SD contenant les informations du sound-deck, ou None
            si aucun sound-deck trouvé.
        """
        if id_sd is None:
            print("ID sound-deck invalide fourni pour la recherche.")
            return None

        try:
            with DBConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_sd, nom, description, date_creation
                        FROM ProjetInfo.SoundDeck
                        WHERE id_sd = %(id_sd)s;
                        """,
                        {"id_sd": id_sd},
                    )
                    res = cursor.fetchone()
                    if res is None:
                        return None

                    return SD(
                        id_sd=res["id_sd"],
                        nom=res["nom"],
                        description=res["description"],
                        date_creation=res["date_creation"],
                    )
        except Exception as e:
            print(f"Erreur lors de la recherche du sound-deck avec ID {id_sd} : {e}")
            return None

    def valider_sd(self, sd: SD) -> bool:
        """
        Valide les données d'entrée pour l'ajout ou la modification d'un sound-deck.

        Parameters
        ----------
        sd : SD
            L'objet SD à valider.

        Returns
        -------
        bool
            True si les données sont valides, False pour des données incorrects.
        """
        if not isinstance(sd.nom, str) or not sd.nom:
            return False
        if not isinstance(sd.description, str):
            return False
        if not isinstance(sd.date_creation, str) or not sd.date_creation:
            return False
        return True
