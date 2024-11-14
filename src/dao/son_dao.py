from dao.db_connection import DBConnection
from business_object.son import Son
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_manuel import Son_Manuel
from business_object.son_continu import Son_Continu
from dao.tag_dao import TagDAO
from view.session import Session
import datetime


class SonDAO:
    """Implémente les méthodes du CRUD pour accéder à la base de données des sons"""

    def time_to_timedelta(self, t: datetime.time) -> datetime.timedelta:
        str_t = t.strftime("%H:%M:%S")
        h = str_t[0] + str_t[1]
        m = str_t[3] + str_t[4]
        s = str_t[6] + str_t[7]
        return datetime.timedelta(
            hours=int(h),
            minutes=int(m),
            seconds=int(s),
        )

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

    def ajouter_son(self, son, schema: str):
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

    def modifier_son(self, son, schema: str):
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

    def modifier_param_son(self, son, schema: str):  # NON TESTED YET
        dict_f_string = {
            "param1": None,
            "param2": None,
            "id_freesound": son.id_freesound,
            "id_scene": Session().scene_to_param.id_scene,
        }
        if isinstance(son, Son_Aleatoire):
            dict_f_string["param1"] = son.cooldown_min
            dict_f_string["param2"] = son.cooldown_max
        elif isinstance(son, Son_Manuel):
            dict_f_string["param1"] = son.start_key
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""
                UPDATE {schema}.Scene_Son
                    SET param1 = %(param1)s, param2 = %(param2)s
                    WHERE id_freesound = %(id_freesound)s AND id_scene = %(id_scene)s;
                """

                cursor.execute(
                    query,
                    dict_f_string,
                )
        return son

    def supprimer_son(self, id_freesound, schema: str):
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

    def consulter_sons(self, schema: str):
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
                    "tags": TagDAO().rechercher_tags_par_son(
                        str(row["id_freesound"]), schema=schema
                    ),
                    "duree": row["duree"],
                }
            )
        return sons_trouves

    def rechercher_par_id_son(self, id_freesound: str, schema: str):
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
            "tags": TagDAO().rechercher_tags_par_son(str(res["id_freesound"]), schema=schema),
            "duree": res["duree"],
        }
        return son_trouve

    def rechercher_sons_par_scene(self, id_scene: str, schema: str):
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
                # On ajoute les sons trouvés dans le dict correspondant à son type
                if row["type"] == "aleatoire":
                    son_dict = {
                        "id_freesound": row["id_freesound"],
                        "nom": row["nom"],
                        "description": row["description"],
                        "duree": self.time_to_timedelta(t=row["duree"]),
                        "tags": TagDAO().rechercher_tags_par_son(
                            str(row["id_freesound"]), schema=schema
                        ),
                        "param1": int(row["param1"]),
                        "param2": int(row["param2"]),
                    }
                    sons_trouves["sons_aleatoires"].append(son_dict)
                elif row["type"] == "continu":
                    son_dict = {
                        "id_freesound": row["id_freesound"],
                        "nom": row["nom"],
                        "description": row["description"],
                        "duree": self.time_to_timedelta(t=row["duree"]),
                        "tags": TagDAO().rechercher_tags_par_son(
                            str(row["id_freesound"]), schema=schema
                        ),
                        "param1": None,
                        "param2": None,
                    }
                    sons_trouves["sons_continus"].append(son_dict)
                elif row["type"] == "manuel":
                    son_dict = {
                        "id_freesound": row["id_freesound"],
                        "nom": row["nom"],
                        "description": row["description"],
                        "duree": self.time_to_timedelta(t=row["duree"]),
                        "tags": TagDAO().rechercher_tags_par_son(
                            str(row["id_freesound"]), schema=schema
                        ),
                        "param1": str(row["param1"]),
                        "param2": None,
                    }
                    sons_trouves["sons_manuels"].append(son_dict)

            return sons_trouves
        except Exception as e:
            print(f"Erreur lors de la récupération des sound-decks : {e}")
            return []

    def ajouter_association_scene_son(self, id_scene: str, son, schema: str):
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
        self, id_scene: str, id_freesound: str, type_son: str, schema: str
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

    def check_if_son_in_scene(self, id_scene: str, id_freesound: str, type_son: str, schema: str):
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

    def get_scenes_of_son_aleatoire(self, id_freesound: str, schema: str):
        """
        Renvoie la liste des scenes qui ont le son mentionné en "aléatoire".
        """
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""SELECT id_scene
                        FROM {schema}.Scene_Son
                        WHERE id_freesound = %(id_freesound)s
                        AND type = "aleatoire";"""
                cursor.execute(
                    query,
                    {"id_freesound": id_freesound},
                )
                res = cursor.fetchall()
        return [row["id_scene"] for row in res]

    def get_scenes_of_son_continu(self, id_freesound: str, schema: str):
        """
        Renvoie la liste des scenes qui ont le son mentionné en "continu".
        """
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""SELECT id_scene
                        FROM {schema}.Scene_Son
                        WHERE id_freesound = %(id_freesound)s
                        AND type = "continu";"""
                cursor.execute(
                    query,
                    {"id_freesound": id_freesound},
                )
                res = cursor.fetchall()
        return [row["id_scene"] for row in res]

    def get_scenes_of_son_manuel(self, id_freesound: str, schema: str):
        """
        Renvoie la liste des scenes qui ont le son mentionné en "manuel".
        """
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f"""SELECT id_scene
                        FROM {schema}.Scene_Son
                        WHERE id_freesound = %(id_freesound)s
                        AND type = "manuel";"""
                cursor.execute(
                    query,
                    {"id_freesound": id_freesound},
                )
                res = cursor.fetchall()
        return [row["id_scene"] for row in res]

    def get_tags_of_son(self, id_freesound: str, schema: str):
        """
        Renvoie la liste des tags de id_freesound
        """
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT nom_tag FROM {schema}.Son_Tag WHERE id_freesound = %(id_freesound)s;",
                    {"id_freesound": id_freesound},
                )
                res = cursor.fetchall()
        return [row["nom_tag"] for row in res]

    def supprimer_toutes_associations_son(self, id_freesound: str, type_son: str, schema: str):
        # Get all scenes having the given son as type_son
        if type_son == "aleatoire":
            scenes_possedants = [
                scene_id
                for scene_id in self.get_scenes_of_son_aleatoire(
                    id_freesound=id_freesound, schema=schema
                )
                if self.check_if_son_in_scene(
                    id_scene=scene_id,
                    id_freesound=id_freesound,
                    type_son="aleatoire",
                    schema=schema,
                )
            ]

        if type_son == "continu":
            scenes_possedants = [
                scene_id
                for scene_id in self.get_scenes_of_son_aleatoire(
                    id_freesound=id_freesound, schema=schema
                )
                if self.check_if_son_in_scene(
                    id_scene=scene_id, id_freesound=id_freesound, type_son="continu", schema=schema
                )
            ]

        if type_son == "manuel":
            scenes_possedants = [
                scene_id
                for scene_id in self.get_scenes_of_son_aleatoire(
                    id_freesound=id_freesound, schema=schema
                )
                if self.check_if_son_in_scene(
                    id_scene=scene_id, id_freesound=id_freesound, type_son="manuel", schema=schema
                )
            ]
        # Delete all associations in scene_son for the given son
        for id_scene in scenes_possedants:
            self.supprimer_association_scene_son(
                id_scene=id_scene, id_freesound=id_freesound, type_son=type_son, schema=schema
            )

        # Get all tags associated with the given son
        tags_inclus = [
            nom_tag
            for nom_tag in self.get_tags_of_son(id_freesound=id_freesound, schema=schema)
            if TagDAO().check_if_son_has_tag(id_freesound=id_freesound, tag=nom_tag, schema=schema)
        ]
        # Delete all associations in son_tag for the given son
        for tag in tags_inclus:
            TagDAO().supprimer_association_son_tag(
                id_freesound=id_freesound, tag=tag, schema=schema
            )
