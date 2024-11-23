import re
import pytest

####
from business_object.sd import SD


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
