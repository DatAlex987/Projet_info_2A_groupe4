from dao.db_connection import DBConnection
from business_object.user import User
from business_object.personne import Personne
from business_object.scene import Scene
from business_object.sd import SD
import datetime
from utils.reset_database import ResetDatabase
from dao.user_dao import UserDAO
from dao.sd_dao import SDDAO
from dao.scene_dao import SceneDAO
from dao.son_dao import SonDAO
from dao.tag_dao import TagDAO
from business_object.son import Son
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_manuel import Son_Manuel
from business_object.son_continu import Son_Continu
from service.session import Session
from service.freesound import Freesound
from service.son_service import SonService
import hashlib
from src.service.scene_service import SceneService
import os
import re
from datetime import timedelta
import pygame
import sys

# ResetDatabase().ResetALL()


def test_delete_scene_if_no_sds():
    scene_dao = SceneDAO()
    id_scene = "scene1"
    schema = "ProjetInfo"

    # Étape 1 : Retirer les associations
    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM ProjetInfo.Sounddeck_Scene WHERE id_scene = %s;",
                (id_scene,),
            )
            connection.commit()

    # Étape 2 : Appeler la méthode de suppression
    result = scene_dao.delete_scene_if_no_sds(id_scene, schema)

    # Étape 3 : Vérifier si la suppression a eu lieu
    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ProjetInfo.Scene WHERE id_scene = %s;", (id_scene,))
            scene = cursor.fetchone()
            assert scene is None, f"La scène {id_scene} n'a pas été supprimée !"
    print(f"Test pour delete_scene_if_no_sds passé : {result}")


def test_delete_sd_if_no_users():
    sd_dao = SDDAO()
    schema = "ProjetInfo"

    # Étape 1 : Retirer les associations
    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM ProjetInfo.User_Sounddeck WHERE id_sd = %s;", (id_sd,))
            connection.commit()

    # Étape 2 : Appeler la méthode de suppression
    result = sd_dao.delete_sd_if_no_users(schema)

    # Étape 3 : Vérifier si la suppression a eu lieu
    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ProjetInfo.Sounddeck WHERE id_sd = %s;", (id_sd,))
            sd = cursor.fetchone()
            assert sd is None, f"La Sounddeck n'a pas été supprimée !"
    print(f"Test pour delete_sd_if_no_users passé : {result}")


def test_delete_son_if_no_scenes():
    son_dao = SonDAO()
    id_son = "son1"
    schema = "ProjetInfo"

    # Étape 1 : Retirer les associations
    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM ProjetInfo.Scene_Son WHERE id_son = %s;", (id_son,))
            connection.commit()

    # Étape 2 : Appeler la méthode de suppression
    result = son_dao.delete_son_if_no_scenes(id_son, schema)

    # Étape 3 : Vérifier si la suppression a eu lieu
    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ProjetInfo.Son WHERE id_son = %s;", (id_son,))
            son = cursor.fetchone()
            assert son is None, f"Le son {id_son} n'a pas été supprimé !"
    print(f"Test pour delete_son_if_no_scenes passé : {result}")


def test_delete_tag_if_no_sons():
    tag_dao = TagDAO()
    nom_tag = "Relaxing"
    schema = "ProjetInfo"

    # Étape 1 : Retirer les associations
    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM ProjetInfo.Son_Tag WHERE nom_tag = %s;", (nom_tag,))
            connection.commit()

    # Étape 2 : Appeler la méthode de suppression
    result = tag_dao.delete_tag_if_no_sons(nom_tag, schema)

    # Étape 3 : Vérifier si la suppression a eu lieu
    with DBConnection(schema=schema).connection as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ProjetInfo.Tag WHERE nom_tag = %s;", (nom_tag,))
            tag = cursor.fetchone()
            assert tag is None, f"Le tag {nom_tag} n'a pas été supprimé !"
    print(f"Test pour delete_tag_if_no_sons passé : {result}")


if __name__ == "__main__":
    # Lancer tous les tests
    test_delete_scene_if_no_sds()
    test_delete_sd_if_no_users()
    test_delete_son_if_no_scenes()
    test_delete_tag_if_no_sons()
