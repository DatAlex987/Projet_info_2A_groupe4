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
                        Scene(
                            id_scene=str(row["id_scene"]),
                            nom=row["nom"],
                            sons_aleatoires=[],  # SANS DOUTE A MODIFIER à L'AVENIR
                            sons_continus=[],  # SANS DOUTE A MODIFIER à L'AVENIR
                            sons_manuels=[],  # SANS DOUTE A MODIFIER à L'AVENIR
                            description=row["description"],
                            date_creation=row["date_creation"],
                        )
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

                Scene_trouvee = Scene(
                    id_scene=str(res["id_scene"]),
                    nom=res["nom"],
                    sons_aleatoires=[],  # SANS DOUTE A MODIFIER à L'AVENIR
                    sons_continus=[],  # SANS DOUTE A MODIFIER à L'AVENIR
                    sons_manuels=[],  # SANS DOUTE A MODIFIER à L'AVENIR
                    description=res["description"],
                    date_creation=res["date_creation"],
                )
        return Scene_trouvee
