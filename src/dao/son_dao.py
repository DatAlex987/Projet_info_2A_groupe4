from dao.db_connection import DBConnection
from business_object.son import Son


class SonDAO:
    """Implémente les méthodes du CRUD pour accéder à la base de données des sons"""

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

    def consulter_sons(self, schema) -> list["Son"]:
        with DBConnection(schema=schema).connection as connection:
            with connection.cursor() as cursor:
                query = f""""
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


# Méthode inutile au final
# def rechercher_par_tags_sons():
#     pass
