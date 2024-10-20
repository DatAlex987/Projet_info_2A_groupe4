from utils.singleton import Singleton
from dao.db_connection import DBConnection
from business_object.son import Son


class SonDAO:
    """Implémente les méthodes du CRUD pour accéder à la base de données des sons"""

    def ajouter_son(self, son):
        with DBConnection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO ProjetInfo.Son (nom, description, duree)
                    VALUES (%(nom)s, %(description)s, %(duree)s)
                    RETURNING id_son;
                    """,
                    {
                        "nom": son.nom,
                        "description": son.description,
                        "duree": son.duree,
                    }
                )
                son.id = cursor.fetchone()["id_son"]
        return son


    def modifier_son(self, son):
        with DBConnection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE son
                    SET nom = %(nom)s, description = %(description)s, duree = %(duree)s
                    WHERE id_son = %(id_son)s;
                    """,
                    {
                        "nom": son.nom,
                        "description": son.description,
                        "duree": son.duree,
                        "id_son": son.id_son
                        }
                )
        return son



    def supprimer_son(self, id_son):
         with DBConnection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM ProjetInfo.Son
                    WHERE id_son = %(id_son)s;
                    """,
                    {"id_son": id_son}
                )


    def consulter_sons(self) -> list['Son']:
        with DBConnection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id_son, nom, description, duree
                    FROM ProjetInfo.Son;
                    """
                )
                res = cursor.fetchall()

                if not res:
                    return []

                sons = [
                    ProjetInfo.Son(
                        id_son=row['id_son'],
                        nom=row['nom'],
                        description=row['description'],
                        duree=row['duree']
                    )
                    for row in res
                ]
        return sons


    def rechercher_par_id_sons(self, id_son):
         with DBConnection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id_son, nom, description, duree
                    FROM ProjetInfo.Son
                    WHERE id_son = %(id_son)s;
                    """,
                    {"id_son": id_son}
                )
                res = cursor.fetchone()

                if res is None:
                    return None

                son = ProjetInfo.Son(
                    id_son=result['id_son'],
                    nom=result['nom'],
                    description=result['description'],
                    duree=result['duree']
                )
        return son





    def rechercher_par_tags_sons():
        pass
