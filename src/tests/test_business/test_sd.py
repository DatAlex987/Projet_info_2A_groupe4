import re
import pytest
from business_object.sd import SD
from business_object.scene import Scene

def test_modifier_nom_sd_succes(sd_kwargs):
    sd_test = SD(**sd_kwargs)
    sd_test.modifier_nom_sd("aventure foraine")
    assert sd_test.nom == "aventure foraine"

def test_modifier_nom_sd_echec(sd_kwargs):
    """Test modifier_nom with invalid input (not a string)"""
    sd_test = SD(**sd_kwargs)
    with pytest.raises(TypeError):
        sd_test.modifier_nom_sd(12345)


def test_modifier_description_sd_succes(sd_kwargs):
    sd_test = SD(**sd_kwargs)
    sd_test.modifier_description_sd("Nouvelle description")
    assert sd_test.description == "Nouvelle description"


def test_modifier_description_sd_echec(sd_kwargs):
    sd_test = SD(**sd_kwargs)
    with pytest.raises(TypeError):
        sd_test.modifier_description_sd(12345)


def test_ajouter_scene_succes(sd_kwargs, scene2_kwargs):
    sd = SD(**sd_kwargs)
    scene_new = Scene(**scene2_kwargs)
    sd.ajouter_scene(scene_new)
    assert scene_new in sd.scenes

def test_ajouter_scene_echec(sd_kwargs):
     sd_test = SD(**sd_kwargs)
     with pytest.raises(TypeError):
        sd_test.ajouter_scene()


def test_retirer_scene()