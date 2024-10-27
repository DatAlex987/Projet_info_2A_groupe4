from dao.db_connection import DBConnection
from business_object.son import Son
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_manuel import Son_Manuel
from business_object.son_continu import Son_Continu


class SonDAO:
    """Implémente les méthodes du CRUD pour accéder à la base de données des sons"""

    def param_of_son(self, son):
        if isinstance(son, Son_Aleatoire):
            return [son.cooldown_min, son.cooldown_max]
        elif isinstance(son, Son_Continu):
            return [None, None]
        elif isinstance(son, Son_Manuel):
            return [son.start_key, None]

    def type_of_son(self, son):
        if isinstance(son, Son_Aleatoire):
            return "aleatoire"
        elif isinstance(son, Son_Continu):
            return "continu"
        elif isinstance(son, Son_Manuel):
            return "manuel"

    def ajouter_son(self, son, schema):
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""
                INSERT INTO {schema}.Son (id_freesound, nom, description, duree)
                    VALUES (%(id_freesound)s, %(nom)s, %(description)s, %(duree)s)
                    RETURNING id_freesound;
                 """
                cursor.execute(
                    query,
                    {
                        "id_freesound": son.id_freesound,
                        "nom": son.nom,
                        "description": son.description,
                        "duree": son.duree,
                    },
                )
                son.id = cursor.fetchone()["id_freesound"]
        return son

    def modifier_son(self, son, schema):
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""
                UPDATE {schema}.Son
                    SET nom = %(nom)s, description = %(description)s, duree = %(duree)s
                    WHERE id_freesound = %(id_freesound)s;
                """

                cursor.execute(
                    query,
                    {
                        "nom": son.nom,
                        "description": son.description,
                        "duree": son.duree,
                        "id_freesound": son.id_freesound,
                    },
                )
        return son

    def supprimer_son(self, id_freesound, schema):
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""
                DELETE FROM {schema}.Son
                    WHERE id_freesound = %(id_freesound)s;
                """

                cursor.execute(
                    query,
                    {"id_freesound": id_freesound},
                )

    def consulter_sons(self, schema):
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""
                 SELECT id_freesound, nom, description, duree
                    FROM {schema}.Son;
                """
                cursor.execute(query)
                res = cursor.fetchall()

                if not res:
                    return []

                sons_trouves = []
                for row in res:
                    sons_trouves.append(
                        {
                            "id_freesound": str(row["id_freesound"]),
                            "nom": row["nom"],
                            "description": row["description"],
                            "duree": row["duree"],
                        }
                    )
        return sons_trouves

    def rechercher_par_id_son(self, id_freesound, schema):
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""
                SELECT id_freesound, nom, description, duree
                    FROM {schema}.Son
                    WHERE id_freesound = %(id_freesound)s;
                """
                cursor.execute(
                    query,
                    {"id_freesound": id_freesound},
                )
                res = cursor.fetchone()

                if res is None:
                    return None

                son_trouve = {
                    "id_freesound": str(res["id_freesound"]),
                    "nom": res["nom"],
                    "description": res["description"],
                    "duree": res["duree"],
                }
        return son_trouve

    def rechercher_sons_par_scene(self, id_scene: str, schema):
        """
        Recherche les sons appartenant à une scène.

        Parameters
        ----------
        id_scene : str
            L'ID de la scène concernée

        Returns
        -------
        dict(list[dict])
            Dictionnaire dont chaque clé correspond à un type de son,
            et chaque valeur est la liste des kwargs des sons trouvés
        """
        if not isinstance(id_scene, str):
            print("ID de la scène invalide pour la recherche.")
            return None

        try:
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:
                    query = f"""
                    SELECT s.id_freesound, s.nom, s.description, s.duree, ss.param1, ss.param2, ss.type
                    FROM {schema}.Scene_Son ss
                    LEFT JOIN {schema}.Son s
                    ON s.id_freesound = ss.id_freesound
                    WHERE ss.id_scene = %(id_scene)s;
                    """

                    cursor.execute(
                        query,
                        {"id_scene": id_scene},
                    )

                    res = cursor.fetchall()

            if not res:
                return {"sons_aleatoires": [], "sons_continus": [], "sons_manuels": []}

            sons_trouves = {"sons_aleatoires": [], "sons_continus": [], "sons_manuels": []}

            # On convertit les sons trouvés en dict
            for row in res:
                son_dict = {
                    "id_freesound": row["id_freesound"],
                    "nom": row["nom"],
                    "description": row["description"],
                    "duree": row["duree"],
                    "param1": row["param1"],
                    "param2": row["param2"],
                }

                # On ajoute les sons trouvés dans le dict correspondant à son type
                if row["type"] == "aleatoire":
                    sons_trouves["sons_aleatoires"].append(son_dict)
                elif row["type"] == "continu":
                    sons_trouves["sons_continus"].append(son_dict)
                elif row["type"] == "manuel":
                    sons_trouves["sons_manuels"].append(son_dict)

            return sons_trouves
        except Exception as e:
            print(f"Erreur lors de la récupération des sound-decks : {e}")
            return []

    def ajouter_association_scene_son(self, id_scene: str, son: Son, schema):
        """
        Ajoute une nouvelle association Scene - Son dans la table d'association.

        Parameters
        ----------
        id_scene : str
            ID de la scène concernée
        Son : Son
            Son concerné

        Returns
        -------
        bool
            True si ajout avec succès, None sinon
        """

        try:
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:
                    query = f"""
                        INSERT INTO {schema}.Scene_Son(id_scene, id_freesound, type, param1, param2)
                        VALUES (%(id_scene)s, %(id_freesound)s, %(type)s, %(param1)s, %(param2)s);
                        """
                    cursor.execute(
                        query,
                        {
                            "id_scene": id_scene,
                            "id_freesound": son.id_freesound,
                            "type": SonDAO().type_of_son(son),
                            "param1": SonDAO().param_of_son(son)[0],
                            "param2": SonDAO().param_of_son(son)[1],
                        },
                    )
            nb_lignes_add = cursor.rowcount
            if nb_lignes_add == 1:
                return True

        except Exception as e:
            print(f"Erreur lors de l'ajout de l'association : {e}")
            return None

    def supprimer_association_scene_son(
        self, id_scene: str, id_freesound: str, type_son: str, schema
    ):
        """
        Supprimer une association Scene - Son dans la table d'association.

        Parameters
        ----------
        id_scene : str
            ID de la scène concernée
        id_freesound : str
            ID du son concerné
        type_son : str
            Type du son dont l'appartenance doit être supprimée

        Returns
        -------
        int
            Nombre de lignes supprimées
        """

        try:
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:
                    query = f"""
                        DELETE FROM {schema}.Scene_Son
                        WHERE id_scene = %(id_scene)s and id_freesound = %(id_freesound)s and type = %(type)s ;
                        """
                    cursor.execute(
                        query,
                        {"id_scene": id_scene, "id_freesound": id_freesound, "type": type_son},
                    )
                    nb_lignes_supp = cursor.rowcount
            return nb_lignes_supp  # Permet notamment de savoir si aucune ligne n'a été trouvée
        except Exception as e:
            print(f"Erreur lors de la suppression de l'association : {e}")
            return None

    def check_if_son_in_scene(self, id_scene: str, id_freesound: str, type_son: str, schema):
        """
        Vérifie si un son appartient à une scène

        Parameters
        ----------
        id_scene : str
            L'ID de la scène à vérifier
        id_freesound : str
            L'ID du son à vérifier
        type_son : str
            Type du son dont l'appartenance à la scène est vérifiée

        Returns
        -------
        bool
            True si le son appartient à la scène, False sinon.
        """
        try:
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:
                    query = f"""
                    SELECT COUNT(*) AS count
                    FROM {schema}.Scene_Son
                    WHERE id_scene = %(id_scene)s AND id_freesound = %(id_freesound)s AND type = %(type)s ;
                    """

                    cursor.execute(
                        query,
                        {
                            "id_scene": id_scene,
                            "id_freesound": id_freesound,
                            "type": type_son,
                        },
                    )

                    # Fetch the result
                    res = cursor.fetchone()
                    # Check if the count is greater than zero
                    return res["count"] > 0

        except Exception as e:
            print(f"Erreur lors de la vérification : {id_scene},{id_freesound},{type_son} : {e}")
            return False
