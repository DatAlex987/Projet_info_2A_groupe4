from business_object.scene import Scene
from dao.db_connection import DBConnection
from dao.son_dao import SonDAO


class SceneDAO:
    """Implémente les méthodes du CRUD pour accéder à la base de données des scènes"""

    def ajouter_scene(self, scene: Scene, schema: str):
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

    def modifier_scene(self, scene: Scene, schema: str):
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

    def supprimer_scene(self, id_scene: str, schema: str):
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

    def consulter_scenes(self, schema: str):
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
                    "sons_aleatoires": SonDAO().rechercher_sons_par_scene(
                        str(row["id_scene"]), schema=schema
                    )["sons_aleatoires"],
                    "sons_continus": SonDAO().rechercher_sons_par_scene(
                        str(row["id_scene"]), schema=schema
                    )["sons_continus"],
                    "sons_manuels": SonDAO().rechercher_sons_par_scene(
                        str(row["id_scene"]), schema=schema
                    )["sons_manuels"],
                    "description": row["description"],
                    "date_creation": row["date_creation"],
                }
            )
        return scenes_trouvees

    def rechercher_par_id_scene(self, id_scene: str, schema: str):
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
            "sons_aleatoires": SonDAO().rechercher_sons_par_scene(
                str(res["id_scene"]), schema=schema
            )["sons_aleatoires"],
            "sons_continus": SonDAO().rechercher_sons_par_scene(
                str(res["id_scene"]), schema=schema
            )["sons_continus"],
            "sons_manuels": SonDAO().rechercher_sons_par_scene(str(res["id_scene"]), schema=schema)[
                "sons_manuels"
            ],
            "description": res["description"],
            "date_creation": res["date_creation"],
        }
        return Scene_trouvee

    def rechercher_scenes_par_sd(self, id_sd: str, schema: str):
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
                        "sons_aleatoires": SonDAO().rechercher_sons_par_scene(
                            str(row["id_scene"]), schema=schema
                        )["sons_aleatoires"],
                        "sons_continus": SonDAO().rechercher_sons_par_scene(
                            str(row["id_scene"]), schema=schema
                        )["sons_continus"],
                        "sons_manuels": SonDAO().rechercher_sons_par_scene(
                            str(row["id_scene"]), schema=schema
                        )["sons_manuels"],
                        "description": row["description"],
                        "date_creation": row["date_creation"],
                    }
                )
            return scenes_trouvees
        except Exception as e:
            print(f"Erreur lors de la récupération des sound-decks : {e}")
            return []

    def ajouter_association_sd_scene(self, id_sd: str, id_scene: str, schema: str):
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
                        VALUES (%(id_sd)s, %(id_scene)s);
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

    def supprimer_association_sd_scene(self, id_sd: str, id_scene: str, schema: str):
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
            return nb_lignes_supp  # Permet en particulier de savoir si aucune ligne n'a été trouvée
        except Exception as e:
            print(f"Erreur lors de la suppression de l'association : {e}")
            return None

    def check_if_scene_in_sd(self, id_sd: str, id_scene: str, schema: str):
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

                    res = cursor.fetchone()
                    return res["count"] > 0

        except Exception as e:
            print(f"Erreur lors de la vérification : {id_scene},{id_sd} : {e}")
            return False

    def get_sds_of_scene(self, id_scene: str, schema: str):
        """
        Renvoie la liste des id des SD qui ont id_scene dedans
        """
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT id_sd FROM {schema}.Sounddeck_Scene WHERE id_scene = %(id_scene)s;",
                    {"id_scene": id_scene},
                )
                res = cursor.fetchall()
        return [row["id_sd"] for row in res]

    def get_sons_aleatoires_of_scene(self, id_scene: str, schema: str):
        """
        Renvoie la liste des id des Sons Aléatoires qui ont id_scene dedans
        """
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""SELECT id_son
                        FROM {schema}.Scene_Son
                        WHERE id_scene = %(id_scene)s
                        AND type = 'aleatoire';"""  # Ces 2 conditions portent sur Son Aleatoires
                cursor.execute(
                    query,
                    {"id_scene": id_scene},
                )
                res = cursor.fetchall()
        return [row["id_son"] for row in res]

    def get_sons_continus_of_scene(self, id_scene: str, schema: str):
        """
        Renvoie la liste des id des Sons Aléatoires qui ont id_scene dedans
        """
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""SELECT id_son
                        FROM {schema}.Scene_Son
                        WHERE id_scene = %(id_scene)s
                        AND type = 'continu';"""  # Ces 2 conditions portent sur Son Continus
                cursor.execute(
                    query,
                    {"id_scene": id_scene},
                )
                res = cursor.fetchall()
        return [row["id_son"] for row in res]

    def get_sons_manuels_of_scene(self, id_scene: str, schema: str):
        """
        Renvoie la liste des id des Sons Aléatoires qui ont id_scene dedans
        """
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""SELECT id_son
                        FROM {schema}.Scene_Son
                        WHERE id_scene = %(id_scene)s
                        AND type = 'manuel';"""  # Ces 2 conditions portent sur Son Manuels
                cursor.execute(
                    query,
                    {"id_scene": id_scene},
                )
                res = cursor.fetchall()
        return [row["id_son"] for row in res]

    def supprimer_toutes_associations_scene(self, id_scene: str, schema: str):
        # On récupère tous les Sd qui possède la scène spécifiée
        sds_possedants = [
            sd_id
            for sd_id in self.get_sds_of_scene(id_scene=id_scene, schema=schema)
            if self.check_if_scene_in_sd(id_sd=sd_id, id_scene=id_scene, schema=schema)
        ]

        # On supprime toutes les associations de SD_Scene qui impliquent la scène
        for id_sd in sds_possedants:
            self.supprimer_association_sd_scene(id_sd=id_sd, id_scene=id_scene, schema=schema)

        # On récup tous les sons aléatoires associés à la scène
        sons_inclus = [
            son_id
            for son_id in self.get_sons_aleatoires_of_scene(id_scene=id_scene, schema=schema)
            if SonDAO().check_if_son_in_scene(
                id_son=son_id, id_scene=id_scene, type_son="aleatoire", schema=schema
            )
        ]

        # On supprime toutes les associations son_alea - scene
        for id_son in sons_inclus:
            SonDAO().supprimer_association_scene_son(
                id_son=id_son, id_scene=id_scene, type_son="aleatoire", schema=schema
            )

        # idem pour sons continus
        sons_inclus = [
            son_id
            for son_id in self.get_sons_continus_of_scene(id_scene=id_scene, schema=schema)
            if SonDAO().check_if_son_in_scene(
                id_son=son_id, id_scene=id_scene, type_son="continu", schema=schema
            )
        ]

        for id_son in sons_inclus:
            SonDAO().supprimer_association_scene_son(
                id_son=id_son, id_scene=id_scene, type_son="continu", schema=schema
            )

        # idem pour sons manuels
        sons_inclus = [
            son_id
            for son_id in self.get_sons_manuels_of_scene(id_scene=id_scene, schema=schema)
            if SonDAO().check_if_son_in_scene(
                id_son=son_id, id_scene=id_scene, type_son="manuel", schema=schema
            )
        ]

        for id_son in sons_inclus:
            SonDAO().supprimer_association_scene_son(
                id_son=id_son, id_scene=id_scene, type_son="manuel", schema=schema
            )

    def delete_scene_if_no_sds(self, schema: str):
        """
        Supprime une scène si elle n'est reliée à aucune Sounddeck.
        """
        all_scenes = self.consulter_scenes(schema=schema)
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                for scene in all_scenes:
                    # On vérifie si des Sounddecks sont liés à la scène
                    cursor.execute(
                        f"SELECT COUNT(*) AS sd_count FROM {schema}.Sounddeck_Scene WHERE id_scene = %(id_scene)s;",
                        {"id_scene": scene["id_scene"]},
                    )
                    sd_count = cursor.fetchone()["sd_count"]

                    # Si aucune Sounddeck n'est liée on supprime la scène
                    if sd_count == 0:
                        cursor.execute(
                            f"DELETE FROM {schema}.Scene WHERE id_scene = %(id_scene)s;",
                            {"id_scene": scene["id_scene"]},
                        )
                        connection.commit()
