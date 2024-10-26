import re
import pytest
from business_object.sd import SD
from business_object.scene import Scene


def test_modifier_nom_sd_succes(sd_kwargs):
    sd_test = SD(**sd_kwargs)
    sd_test.modifier_nom_sd("aventure foraine")
    assert sd_test.nom == "aventure foraine"


@pytest.mark.parametrize(
    "new_nom, expected_error, error_type",
    [
        (15, "Le nom doit etre une instance de str.", TypeError),
        ([], "Le nom doit etre une instance de str.", TypeError),
    ],
)
def test_modifier_nom_sd_echec(sd_kwargs, new_nom, expected_error, error_type):
    with pytest.raises(error_type, match=re.escape(expected_error)):
        sd_test = SD(**sd_kwargs)
        sd_test.modifier_nom_sd(new_nom)


def test_modifier_description_sd_succes(sd_kwargs):
    sd_test = SD(**sd_kwargs)
    sd_test.modifier_description_sd("Nouvelle description")
    assert sd_test.description == "Nouvelle description"


@pytest.mark.parametrize(
    "new_desc, expected_error, error_type",
    [
        (123, "La nouvelle description doit etre une instance de str.", TypeError),
        ({}, "La nouvelle description doit etre une instance de str.", TypeError),
    ],
)
def test_modifier_description_echec(sd_kwargs, new_desc, expected_error, error_type):
    with pytest.raises(error_type, match=re.escape(expected_error)):
        sd_test = SD(**sd_kwargs)
        sd_test.modifier_description_sd(new_desc)


def test_ajouter_scene_succes(sd_kwargs, scene2_kwargs):
    sd_test = SD(**sd_kwargs)
    new_scene = Scene(**scene2_kwargs)
    sd_test.ajouter_scene(new_scene)
    assert new_scene in sd_test.scenes


@pytest.mark.parametrize(
    "new_scene, expected_error, error_type",
    [
        (123, "La nouvelle scène doit etre une instance de Scene.", TypeError),
        ({}, "La nouvelle scène doit etre une instance de Scene.", TypeError),
    ],
)
def test_ajouter_scene_echec(sd_kwargs, new_scene, expected_error, error_type):
    with pytest.raises(error_type, match=re.escape(expected_error)):
        sd_test = SD(**sd_kwargs)
        sd_test.ajouter_scene(new_scene)


def test_retirer_scene_succes(sd_kwargs, scene1_kwargs):
    sd_test = SD(**sd_kwargs)
    scene = Scene(**scene1_kwargs)
    sd_test.retirer_scene(scene)
    assert scene not in sd_test.scenes


@pytest.mark.parametrize(
    "scene, expected_error, error_type",
    [
        (123, "La scène doit etre une instance de Scene.", TypeError),
        ({}, "La scène doit etre une instance de Scene.", TypeError),
    ],
)
def test_retirer_scene_echec(sd_kwargs, scene, expected_error, error_type):
    with pytest.raises(error_type, match=re.escape(expected_error)):
        sd_test = SD(**sd_kwargs)
        sd_test.retirer_scene(scene)
