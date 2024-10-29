from utils.singleton import Singleton
from dao.db_connection import DBConnection
from business_object.sd import SD
import datetime
from dao.scene_dao import SceneDAO


class SDDAO(metaclass=Singleton):
    """Implémente les méthodes du CRUD pour accéder à la base de données des sound-decks"""

    def ajouter_sd(self, sd: SD, schema) -> SD:
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

        try:
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:
                    query = f"""
                     INSERT INTO {schema}.SoundDeck(id_sd, nom, description, date_creation)
                        VALUES (%(id_sd)s, %(nom)s, %(description)s, %(date_creation)s)
                        RETURNING id_sd;
                    """
                    cursor.execute(
                        query,
                        {
                            "id_sd": sd.id_sd,
                            "nom": sd.nom,
                            "description": sd.description,
                            "date_creation": sd.date_creation,
                        },
                    )

            return sd
        except Exception as e:
            print(f"Erreur lors de l'ajout du sound-deck : {e}")
            return None

    def modifier_sd(self, sd: SD, schema) -> SD:
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

        try:
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:

                    query = f"""
                    UPDATE {schema}.SoundDeck
                        SET nom = %(nom)s, description = %(description)s, date_creation = %(date_creation)s
                        WHERE id_sd = %(id_sd)s;
                    """
                    cursor.execute(
                        query,
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

    def supprimer_sd(self, id_sd: int, schema) -> bool:
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
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:
                    query = f"""
                     DELETE FROM {schema}.SoundDeck
                        WHERE id_sd = %(id_sd)s;
                    """
                    cursor.execute(
                        query,
                        {"id_sd": id_sd},
                    )
                    return cursor.rowcount > 0
        except Exception as e:
            print(f"Erreur lors de la suppression du sound-deck avec ID {id_sd} : {e}")
            return False

    def consulter_sds(self, schema) -> list:
        """
        Récupère la liste de tous les sound-decks dans la base de données.

        Returns
        -------
        list
            Une liste d'objets SD contenant les informations des sound-decks.
        """
        try:
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:
                    query = f"""
                    SELECT id_sd, nom, description, date_creation
                        FROM {schema}.SoundDeck;
                    """

                    cursor.execute(query)
                    res = cursor.fetchall()

            if not res:
                return []

            sd_trouves = []

            for row in res:
                sd_trouves.append(
                    {
                        "id_sd": str(row["id_sd"]),
                        "nom": row["nom"],
                        "scenes": SceneDAO().rechercher_scenes_par_sd(
                            str(row["id_sd"]), schema=schema
                        ),
                        "description": row["description"],
                        "date_creation": row["date_creation"],
                    }
                )
            return sd_trouves
        except Exception as e:
            print(f"Erreur lors de la récupération des sound-decks : {e}")
            return []

    def rechercher_par_id_sd(self, id_sd: int, schema) -> SD:
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
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:
                    query = f"""
                    SELECT id_sd, nom, description, date_creation
                        FROM {schema}.SoundDeck
                        WHERE id_sd = %(id_sd)s;
                    """

                    cursor.execute(
                        query,
                        {"id_sd": id_sd},
                    )

                    res = cursor.fetchone()
            if res is None:
                return None

            return {
                "id_sd": res["id_sd"],
                "nom": res["nom"],
                "description": res["description"],
                "date_creation": res["date_creation"],
                "scenes": SceneDAO().rechercher_scenes_par_sd(
                    str(res["id_sd"]), schema=schema
                ),  # A AJOUTER PLUS TARD
            }
        except Exception as e:
            print(f"Erreur lors de la recherche du sound-deck avec ID {id_sd} : {e}")
            return None

    def rechercher_sds_par_user(self, id_user: str, schema):
        """
        Recherche les sound-decks dans la base de données d'un utilisateur.

        Parameters
        ----------
        id_user : str
            L'ID de l'utilisateur concerné

        Returns
        -------
        list[dict]
            Liste des kwargs des sound-decks trouvés
        """
        if not isinstance(id_user, str):
            print("ID de l'utilisateur invalide pour la recherche.")
            return None

        try:
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:
                    query = f"""
                    SELECT Sounddeck.id_sd, nom, description, date_creation
                    FROM {schema}.SoundDeck
                    LEFT JOIN {schema}.User_Sounddeck
                    ON {schema}.SoundDeck.id_sd = {schema}.User_Sounddeck.id_sd
                    WHERE id_user = %(id_user)s;
                    """

                    cursor.execute(
                        query,
                        {"id_user": id_user},
                    )

                    res = cursor.fetchall()
            if not res:
                return []

            sd_trouves = []

            for row in res:
                sd_trouves.append(
                    {
                        "id_sd": str(row["id_sd"]),
                        "nom": row["nom"],
                        "scenes": SceneDAO().rechercher_scenes_par_sd(
                            str(row["id_sd"]), schema=schema
                        ),  # A AJOUTER PLUS TARD
                        "description": row["description"],
                        "date_creation": row["date_creation"],
                    }
                )
            return sd_trouves
        except Exception as e:
            print(f"Erreur lors de la récupération des sound-decks : {e}")
            return []

    def ajouter_association_user_sd(self, id_user: str, id_sd: str, schema):
        """
        Ajoute une nouvelle association User - SD dans la table d'association.

        Parameters
        ----------
        id_sd : str
            ID du Sound-deck concerné
        id_user : str
            ID du User concerné

        Returns
        -------
        bool
            True si ajout avec succès, None sinon
        """

        try:
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:
                    query = f"""
                        INSERT INTO {schema}.User_Sounddeck(id_user, id_sd)
                        VALUES (%(id_user)s, %(id_sd)s);
                        """
                    cursor.execute(
                        query,
                        {
                            "id_user": id_user,
                            "id_sd": id_sd,
                        },
                    )
                    nb_lignes_add = cursor.rowcount
            if nb_lignes_add == 1:
                return True

        except Exception as e:
            print(f"Erreur lors de l'ajout de l'association : {e}")
            return None

    def supprimer_association_user_sd(self, id_user: str, id_sd: str, schema):
        """
        Supprimer une association User - SD dans la table d'association.

        Parameters
        ----------
        id_sd : str
            ID du Sound-deck concerné
        id_user : str
            ID du User concerné

        Returns
        -------
        int
            Nombre de lignes supprimées
        """

        try:
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:
                    query = f"""
                        DELETE FROM {schema}.User_Sounddeck
                        WHERE id_user = %(id_user)s and id_sd = %(id_sd)s;
                        """
                    cursor.execute(
                        query,
                        {
                            "id_user": id_user,
                            "id_sd": id_sd,
                        },
                    )
                    nb_lignes_supp = cursor.rowcount
            return nb_lignes_supp  # Permet notamment de savoir si aucune ligne n'a été trouvée
        except Exception as e:
            print(f"Erreur lors de la suppression de l'association : {e}")
            return None

    def check_if_sd_in_user(self, id_user: str, id_sd: str, schema):
        """
        Vérifie si un sound-deck appartient à un utilisateur.

        Parameters
        ----------
        id_user : str
            L'ID de l'utilisateur à vérifier.
        id_sd : str
            L'ID du sound-deck à vérifier.

        Returns
        -------
        bool
            True si le sound-deck appartient à l'utilisateur, False sinon.
        """
        try:
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:
                    query = f"""
                    SELECT COUNT(*) AS count
                    FROM {schema}.User_Sounddeck
                    WHERE id_user = %(id_user)s AND id_sd = %(id_sd)s;
                    """

                    cursor.execute(
                        query,
                        {
                            "id_user": id_user,
                            "id_sd": id_sd,
                        },
                    )

                    # Fetch the result
                    res = cursor.fetchone()
                    # Check if the count is greater than zero
                    return res["count"] > 0

        except Exception as e:
            print(
                f"Erreur lors de la vérification de l'appartenance du sound-deck {id_sd} à l'utilisateur {id_user} : {e}"
            )
            return False
