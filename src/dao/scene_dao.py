from dao.db_connection import DBConnection
from business_object.scene import Scene


class SceneDAO:
    """Implémente les méthodes du CRUD pour accéder à la base de données des scènes"""

    def ajouter_scene(self, scene, schema):
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""
                INSERT INTO {schema}.Scene(id_scene, nom, description, date_creation)
                    VALUES (%(id_scene)s, %(nom)s, %(description)s, %(date_creation)s)
                    RETURNING id_scene;
                """
                cursor.execute(
                    query,
                    {
                        "id_scene": scene.id_scene,
                        "nom": scene.nom,
                        "description": scene.description,
                        "date_creation": scene.date_creation,
                    },
                )
                scene.id = cursor.fetchone()["id_scene"]
        return scene

    def modifier_scene(self, scene, schema):
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""
                UPDATE {schema}.Scene
                    SET nom = %(nom)s, description = %(description)s,
                    date_creation = %(date_creation)s
                    WHERE id_scene = %(id_scene)s;
                """
                cursor.execute(
                    query,
                    {
                        "nom": scene.nom,
                        "description": scene.description,
                        "date_creation": scene.date_creation,
                        "id_scene": scene.id_scene,
                    },
                )
        return scene

    def supprimer_scene(self, id_scene, schema):
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""
                DELETE FROM {schema}.Scene
                    WHERE id_scene = %(id_scene)s;
                """
                cursor.execute(
                    query,
                    {"id_scene": id_scene},
                )

    def consulter_scenes(self, schema):
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""
                SELECT id_scene, nom, description, date_creation
                    FROM {schema}.Scene;
                """
                cursor.execute(query)
                res = cursor.fetchall()

                if not res:
                    return []

                scenes_trouvees = []

                for row in res:
                    scenes_trouvees.append(
                        {
                            "id_scene": str(row["id_scene"]),
                            "nom": row["nom"],
                            "sons_aleatoires": [],  # SANS DOUTE A MODIFIER à L'AVENIR
                            "sons_continus": [],  # SANS DOUTE A MODIFIER à L'AVENIR
                            "sons_manuels": [],  # SANS DOUTE A MODIFIER à L'AVENIR
                            "description": row["description"],
                            "date_creation": row["date_creation"],
                        }
                    )
        return scenes_trouvees

    def rechercher_par_id_scenes(self, id_scene, schema):
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""
                SELECT id_scene, nom, description, date_creation
                    FROM {schema}.Scene
                    WHERE id_scene = %(id_scene)s;
                """
                cursor.execute(
                    query,
                    {"id_scene": id_scene},
                )
                res = cursor.fetchone()
                if res is None:
                    return None

                Scene_trouvee = {
                    "id_scene": str(res["id_scene"]),
                    "nom": res["nom"],
                    "sons_aleatoires": [],  # SANS DOUTE A MODIFIER à L'AVENIR
                    "sons_continus": [],  # SANS DOUTE A MODIFIER à L'AVENIR
                    "sons_manuels": [],  # SANS DOUTE A MODIFIER à L'AVENIR
                    "description": res["description"],
                    "date_creation": res["date_creation"],
                }
        return Scene_trouvee

    def rechercher_scenes_par_sd(self, id_sd: str, schema):  # NOT CHECKED YET
        """
        Recherche les scenes appartenant à un SD.

        Parameters
        ----------
        id_sd : str
            L'ID du SD concerné

        Returns
        -------
        list[dict]
            Liste des kwargs des scènes trouvées
        """
        if not isinstance(id_sd, str):
            print("ID du SD invalide pour la recherche.")
            return None

        try:
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:
                    query = f"""
                    SELECT Scene.id_scene, nom, description, date_creation
                    FROM {schema}.Scene
                    LEFT JOIN {schema}.Sounddeck_Scene
                    ON {schema}.Scene.id_scene = {schema}.Sounddeck_Scene.id_scene
                    WHERE id_sd = %(id_sd)s;
                    """

                    cursor.execute(
                        query,
                        {"id_sd": id_sd},
                    )

                    res = cursor.fetchall()

                if not res:
                    return []

                scenes_trouvees = []

                for row in res:
                    scenes_trouvees.append(
                        {
                            "id_scene": str(row["id_scene"]),
                            "nom": row["nom"],
                            "sons_aleatoires": [],  # SANS DOUTE A MODIFIER à L'AVENIR
                            "sons_continus": [],  # SANS DOUTE A MODIFIER à L'AVENIR
                            "sons_manuels": [],  # SANS DOUTE A MODIFIER à L'AVENIR
                            "description": row["description"],
                            "date_creation": row["date_creation"],
                        }
                    )
                return scenes_trouvees
        except Exception as e:
            print(f"Erreur lors de la récupération des sound-decks : {e}")
            return []

    def ajouter_association_sd_scene(self, id_sd: str, id_scene: str, schema):  # NOT CHECKED YET
        """
        Ajoute une nouvelle association SD - Scene dans la table d'association.

        Parameters
        ----------
        id_sd : str
            ID du Sound-deck concerné
        id_scene : str
            ID de la scène concernée

        Returns
        -------
        bool
            True si ajout avec succès, None sinon
        """

        try:
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:
                    query = f"""
                        INSERT INTO {schema}.Sounddeck_Scene(id_sd, id_scene)
                        VALUES (%(id_sd)s, %(id_d=scene)s);
                        """
                    cursor.execute(
                        query,
                        {
                            "id_sd": id_sd,
                            "id_scene": id_scene,
                        },
                    )
                    nb_lignes_add = cursor.rowcount
            if nb_lignes_add == 1:
                return True

        except Exception as e:
            print(f"Erreur lors de l'ajout de l'association : {e}")
            return None

    def supprimer_association_sd_scene(self, id_sd: str, id_scene: str, schema):  # NOT CHECKED YET
        """
        Supprimer une association SD - Scene dans la table d'association.

        Parameters
        ----------
        id_sd : str
            ID du Sound-deck concerné
        id_scene : str
            ID de la scène concernée

        Returns
        -------
        int
            Nombre de lignes supprimées
        """

        try:
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:
                    query = f"""
                        DELETE FROM {schema}.Sounddeck_Scene
                        WHERE id_sd = %(id_sd)s and id_scene = %(id_scene)s;
                        """
                    cursor.execute(
                        query,
                        {
                            "id_sd": id_sd,
                            "id_scene": id_scene,
                        },
                    )
                    nb_lignes_supp = cursor.rowcount
            return nb_lignes_supp  # Permet notamment de savoir si aucune ligne n'a été trouvée
        except Exception as e:
            print(f"Erreur lors de la suppression de l'association : {e}")
            return None

    def check_if_scene_in_sd(self, id_sd: str, id_scene: str, schema):  # NOT CHECKED YET
        """
        Vérifie si une scène appartient à un SD.

        Parameters
        ----------
        id_sd : str
            L'ID du SD à vérifier.
        id_scene : str
            L'ID de la scène à vérifier.

        Returns
        -------
        bool
            True si la scène appartient au SD, False sinon.
        """
        try:
            with DBConnection(schema=schema).connection as conn:
                with conn.cursor() as cursor:
                    query = f"""
                    SELECT COUNT(*) AS count
                    FROM {schema}.Sounddeck_Scene
                    WHERE id_sd = %(id_sd)s AND id_scene = %(id_scene)s;
                    """

                    cursor.execute(
                        query,
                        {
                            "id_sd": id_sd,
                            "id_scene": id_scene,
                        },
                    )

                    # Fetch the result
                    res = cursor.fetchone()
                    # Check if the count is greater than zero
                    return res["count"] > 0

        except Exception as e:
            print(f"Erreur lors de la vérification : {id_scene},{id_sd} : {e}")
            return False
