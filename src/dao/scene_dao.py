from utils.singleton import Singleton
from dao.db_connection import DBConnection
from business_object.scene import Scene


class SceneDAO:
    """Implémente les méthodes du CRUD pour accéder à la base de données des scènes"""

    def ajouter_scene(self, scene):
        with DBConnection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO ProjetInfo.Scene(nom, description, date_creation)
                    VALUES (%(nom)s, %(description)s, %(date_creation)s)
                    RETURNING id_scene;
                    """,
                    {
                        "nom": scene.nom,
                        "description": scene.description,
                        "date_creation": scene.date_creation,
                    },
                )
                scene.id = cursor.fetchone()["id_scene"]
        return scene

    def modifier_scene(self, scene):
        with DBConnection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE scene
                    SET nom = %(nom)s, description = %(description)s, date_creation = %(date_creation)s
                    WHERE id_scene = %(id_scene)s;
                    """,
                    {
                        "nom": scene.nom,
                        "description": scene.description,
                        "date_creation": scene.duree,
                        "id_scene": scene.id_scene,
                    },
                )
        return scene

    def supprimer_scene(self, id_scene):
        with DBConnection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM ProjetInfo.Scene
                    WHERE id_scene = %(id_scene)s;
                    """,
                    {"id_scene": id_scene},
                )

    def consulter_scenes(self, scene):
        with DBConnection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id_scene, nom, description, date_creation
                    FROM ProjetInfo.Scene;
                    """
                )
                res = cursor.fetchall()

                if not res:
                    return []

                scenes_trouvees = []

                for row in res:
                    scenes_trouvees.append(
                        Scene(
                            id_scene=row["id_scene"],
                            nom=row["nom"],
                            description=row["description"],
                            date_creation=row["date_creation"],
                        )
                    )
        return scenes_trouvees

    def rechercher_par_id_scenes(self, id_scene):
        with DBConnection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id_scene, nom, description, date_creation
                    FROM ProjetInfo.Scene
                    WHERE id_scene = %(id_scene)s;
                    """,
                    {"id_scene": id_scene},
                )
                res = cursor.fetchone()
                if res is None:
                    return None

                Scene_trouvee = Scene(
                    id_scene=res["id_scene"],
                    nom=res["nom"],
                    description=res["description"],
                    date_creation=res["date_creation"],
                )
        return Scene_trouvee
