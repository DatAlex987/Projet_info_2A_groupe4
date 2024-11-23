import pytest
import re

####
from business_object.scene import Scene
from business_object.son_aleatoire import Son_Aleatoire
from business_object.son_continu import Son_Continu
from business_object.son_manuel import Son_Manuel


def test_modifier_nom_succes(scene1_kwargs):
    scene_test = Scene(**scene1_kwargs)
    scene_test.modifier_nom("Nouvelle Forêt")
    assert scene_test.nom == "Nouvelle Forêt"


@pytest.mark.parametrize(
    "new_nom, expected_error, error_type",
    [
        (15, "Le nouveau nom doit etre une instance de str.", TypeError),
        ([], "Le nouveau nom doit etre une instance de str.", TypeError),
    ],
)
def test_modifier_nom_echec(scene1_kwargs, new_nom, expected_error, error_type):
    with pytest.raises(error_type, match=re.escape(expected_error)):
        scene_test = Scene(**scene1_kwargs)
        scene_test.modifier_nom(new_nom)


def test_modifier_description_succes(scene1_kwargs):
    scene_test = Scene(**scene1_kwargs)
    scene_test.modifier_description("Ceci est une nouvelle description")
    assert scene_test.description == "Ceci est une nouvelle description"


@pytest.mark.parametrize(
    "new_desc, expected_error, error_type",
    [
        (123, "La nouvelle description doit etre une instance de str.", TypeError),
        ({}, "La nouvelle description doit etre une instance de str.", TypeError),
    ],
)
def test_modifier_description_echec(scene1_kwargs, new_desc, expected_error, error_type):
    with pytest.raises(error_type, match=re.escape(expected_error)):
        scene_test = Scene(**scene1_kwargs)
        scene_test.modifier_description(new_desc)


def test_ajouter_son_aleatoire_succes(scene1_kwargs, son_aleatoire2_kwargs):
    scene_test = Scene(**scene1_kwargs)
    Son_alea_test = Son_Aleatoire(**son_aleatoire2_kwargs)
    scene_test.ajouter_son_aleatoire(Son_alea_test)
    assert scene_test.sons_aleatoires[1] == Son_alea_test


@pytest.mark.parametrize(
    "new_son, expected_error, error_type",
    [
        (123, "Le nouveau son doit etre une instance de son aléatoire.", TypeError),
        ({}, "Le nouveau son doit etre une instance de son aléatoire.", TypeError),
    ],
)
def test_ajouter_son_aleatoire_echec(
    scene1_kwargs, son_aleatoire1_kwargs, new_son, expected_error, error_type
):
    with pytest.raises(error_type, match=re.escape(expected_error)):
        scene_test = Scene(**scene1_kwargs)
        scene_test.ajouter_son_aleatoire(new_son)


def test_ajouter_son_continu_succes(scene1_kwargs, son_continu2_kwargs):
    scene_test = Scene(**scene1_kwargs)
    Son_continu_test = Son_Continu(**son_continu2_kwargs)
    scene_test.ajouter_son_continu(Son_continu_test)
    assert scene_test.sons_continus[1] == Son_continu_test


@pytest.mark.parametrize(
    "new_son, expected_error, error_type",
    [
        (123, "Le nouveau son doit etre une instance de son continu.", TypeError),
        ({}, "Le nouveau son doit etre une instance de son continu.", TypeError),
    ],
)
def test_ajouter_son_continu_echec(
    scene1_kwargs, son_continu1_kwargs, new_son, expected_error, error_type
):
    with pytest.raises(error_type, match=re.escape(expected_error)):
        scene_test = Scene(**scene1_kwargs)
        scene_test.ajouter_son_continu(new_son)


def test_ajouter_son_manuel_succes(scene1_kwargs, son_manuel2_kwargs):
    scene_test = Scene(**scene1_kwargs)
    Son_manuel_test = Son_Manuel(**son_manuel2_kwargs)
    scene_test.ajouter_son_manuel(Son_manuel_test)
    assert scene_test.sons_manuels[1] == Son_manuel_test


@pytest.mark.parametrize(
    "new_son, expected_error, error_type",
    [
        (123, "Le nouveau son doit etre une instance de son manuel.", TypeError),
        ({}, "Le nouveau son doit etre une instance de son manuel.", TypeError),
    ],
)
def test_ajouter_son_manuel_echec(
    scene1_kwargs, son_manuel1_kwargs, new_son, expected_error, error_type
):
    with pytest.raises(error_type, match=re.escape(expected_error)):
        scene_test = Scene(**scene1_kwargs)
        scene_test.ajouter_son_manuel(new_son)


"""def test_supprimer_son_aleatoire_succes(scene1_kwargs, son_aleatoire2_kwargs):
    scene_test = Scene(**scene1_kwargs)
    Son_alea_suppr = Son_Aleatoire(**son_aleatoire2_kwargs)
    scene_test.ajouter_son_aleatoire(
        Son_alea_suppr
    )  # Pour faire référence exactement au même objet (on sait que ajouter_son_alea fonctionne)
    scene_test.supprimer_son_aleatoire(Son_alea_suppr)
    assert Son_alea_suppr not in scene_test.sons_aleatoires


def test_supprimer_son_continu_succes(scene1_kwargs, son_continu2_kwargs):
    scene_test = Scene(**scene1_kwargs)
    Son_continu_suppr = Son_Continu(**son_continu2_kwargs)
    scene_test.ajouter_son_continu(
        Son_continu_suppr
    )  # Pour faire référence exactement au même objet (on sait que ajouter_son_continu fonctionne)
    scene_test.supprimer_son_continu(Son_continu_suppr)
    assert Son_continu_suppr not in scene_test.sons_continus


def test_supprimer_son_manuel_succes(scene1_kwargs, son_manuel2_kwargs):
    scene_test = Scene(**scene1_kwargs)
    Son_manuel_suppr = Son_Manuel(**son_manuel2_kwargs)
    scene_test.ajouter_son_manuel(
        Son_manuel_suppr
    )  # Pour faire référence exactement au même objet (on sait que ajouter_son_alea fonctionne)
    scene_test.supprimer_son_manuel(Son_manuel_suppr)
    assert Son_manuel_suppr not in scene_test.sons_manuels"""
