from utils.singleton import Singleton
from dao.db_connection import DBConnection
from business_object.son import Son


class SonDAO:
    """Implémente les méthodes du CRUD pour accéder à la base de données des sons"""

    def ajouter_son(self, son, schema):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO %(schema)s.Son (id_freesound, nom, description, duree)
                    VALUES (%(id_freesound)s, %(nom)s, %(description)s, %(duree)s)
                    RETURNING id_freesound;
                    """,
                    {
                        "schema": schema,
                        "id_freesound": son.id_freesound,
                        "nom": son.nom,
                        "description": son.description,
                        "duree": son.duree,
                    },
                )
                son.id = cursor.fetchone()["id_freesound"]
        return son

    def modifier_son(self, son, schema):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE %(schema)s.Son
                    SET nom = %(nom)s, description = %(description)s, duree = %(duree)s
                    WHERE id_freesound = %(id_freesound)s;
                    """,
                    {
                        "schema": schema,
                        "nom": son.nom,
                        "description": son.description,
                        "duree": son.duree,
                        "id_freesound": son.id_freesound,
                    },
                )
        return son

    def supprimer_son(self, id_freesound, schema):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM %(schema)s.Son
                    WHERE id_freesound = %(id_freesound)s;
                    """,
                    {"schema": schema, "id_freesound": id_freesound},
                )

    def consulter_sons(self, schema) -> list["Son"]:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id_freesound, nom, description, duree
                    FROM %(schema)s.Son;
                    """
                )
                res = cursor.fetchall()

                if not res:
                    return []

                sons = []
                for row in res:
                    sons.append(
                        Son(
                            id_freesound=row["id_freesound"],
                            nom=row["nom"],
                            description=row["description"],
                            duree=row["duree"],
                        )
                    )
        return sons

    def rechercher_par_id_sons(self, id_freesound, schema):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id_freesound, nom, description, duree
                    FROM %(schema)s.Son
                    WHERE id_freesound = %(id_freesound)s;
                    """,
                    {"id_freesound": id_freesound},
                )
                res = cursor.fetchone()

                if res is None:
                    return None

                son = Son(
                    id_freesound=res["id_freesound"],
                    nom=res["nom"],
                    description=res["description"],
                    duree=res["duree"],
                )
        return son

    def rechercher_par_tags_sons():
        pass
