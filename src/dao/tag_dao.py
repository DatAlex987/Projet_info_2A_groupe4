from dao.db_connection import DBConnection
from business_object.son import Son


class TagDAO:

    def ajouter_tag(self, tag: str, schema: str):
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""
                INSERT INTO {schema}.Tag(nom_tag)
                    VALUES (%(nom_tag)s)
                    RETURNING non_tag;
                """
                cursor.execute(
                    query,
                    {
                        "nom_tag": tag,
                    },
                )
        return tag

    def supprimer_tag(self, tag: str, schema: str):
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""
                DELETE FROM {schema}.Tag
                    WHERE nom_tag = %(nom_tag)s;
                """
                cursor.execute(
                    query,
                    {"nom_tag": tag},
                )

    def consulter_tags(self, schema: str):
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""
                SELECT nom_tag
                    FROM {schema}.Tag;
                """
                cursor.execute(query)
                res = cursor.fetchall()

                if not res:
                    return []

                tags_trouves = []

                for row in res:
                    tags_trouves.append(row["nom_tag"])
        return tags_trouves

    def rechercher_tags_par_son(self, id_freesound: str, schema: str):
        """
        Recherche les tags appartenant à un son.

        Parameters
        ----------
        id_freesound : str
            L'ID du son concerné

        Returns
        -------
        list[str]
            Liste des tags trouvés
        """
        if not isinstance(id_freesound, str):
            print("ID du son invalide pour la recherche.")
            return None

        try:
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:
                    query = f"""
                    SELECT nom_tag
                    FROM {schema}.Son_tag
                    WHERE id_freesound = %(id_freesound)s;
                    """

                    cursor.execute(
                        query,
                        {"id_freesound": id_freesound},
                    )

                    res = cursor.fetchall()

                if not res:
                    return []

                tags_trouves = []

                for row in res:
                    tags_trouves.append(row["nom_tag"])
                return tags_trouves
        except Exception as e:
            print(f"Erreur lors de la récupération des sound-decks : {e}")
            return []

    def ajouter_association_son_tag(self, id_freesound: str, tag: str, schema: str):
        """
        Ajoute une nouvelle association Son - Tag dans la table d'association.

        Parameters
        ----------
        id_freesound : str
            ID du son concerné
        tag : str
            tag concerné

        Returns
        -------
        bool
            True si ajout avec succès, None sinon
        """
        try:
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:
                    query = f"""
                            INSERT INTO {schema}.Son_tag(id_freesound, nom_tag)
                            VALUES (%(id_freesound)s, %(nom_tag)s);
                            """
                    cursor.execute(
                        query,
                        {
                            "id_freesound": id_freesound,
                            "nom_tag": tag,
                        },
                    )
                    nb_lignes_add = cursor.rowcount
                    if nb_lignes_add == 1:
                        return True
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'association : {e}")
            return None

    def supprimer_association_son_tag(self, id_freesound: str, tag: str, schema: str):
        """
        Supprimer une association Son - Tag dans la table d'association.

        Parameters
        ----------
        id_freesound : str
            ID du son concerné
        tag : str
            tag concernée

        Returns
        -------
        int
            Nombre de lignes supprimées
        """

        try:
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:
                    query = f"""
                        DELETE FROM {schema}.Son_Tag
                        WHERE id_freesound = %(id_freesound)s and nom_tag = %(nom_tag)s;
                        """
                    cursor.execute(
                        query,
                        {
                            "id_freesound": id_freesound,
                            "nom_tag": tag,
                        },
                    )
                    nb_lignes_supp = cursor.rowcount
            return nb_lignes_supp  # Permet notamment de savoir si aucune ligne n'a été trouvée
        except Exception as e:
            print(f"Erreur lors de la suppression de l'association : {e}")
            return None

    def check_if_son_has_tag(self, id_freesound: str, tag: str, schema: str):
        """
        Vérifie si un son possède un tag

        Parameters
        ----------
        id_freesound : str
            L'ID du son à vérifier.
        tag : str
           tag à vérifier.

        Returns
        -------
        bool
            True si le son possède le tag, False sinon.
        """
        try:
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:
                    query = f"""
                    SELECT COUNT(*) AS count
                    FROM {schema}.Son_Tag
                    WHERE id_freesoung = %(id_freesound)s AND nom_tag = %(nom_tag)s;
                    """

                    cursor.execute(
                        query,
                        {
                            "id_freesound": id_freesound,
                            "nom_tag": tag,
                        },
                    )

                    # Fetch the result
                    res = cursor.fetchone()
                    # Check if the count is greater than zero
                    return res["count"] > 0

        except Exception as e:
            print(f"Erreur lors de la vérification : {id_freesound},{tag} : {e}")
            return False
