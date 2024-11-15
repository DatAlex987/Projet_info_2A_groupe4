import pytest
from business_object.son_aleatoire import Son_Aleatoire
import datetime


def test_initialisation_son_aleatoire(son_aleatoire1_kwargs):
    """Test de l'initialisation de Son_Aleatoire avec la première fixture."""
    son = Son_Aleatoire(**son_aleatoire1_kwargs)

    assert son.nom == "Ambiance de forêt"
    assert son.description == "Son de fond de forêt calme"
    assert son.duree == datetime.timedelta(seconds=60)
    assert son.id_freesound == "787956"
    assert son.tags == ["nature", "calm", "forest"]
    assert son.cooldown_min == 5
    assert son.cooldown_max == 10


def test_modifier_cooldown_min(son_aleatoire1_kwargs):
    """Test de la méthode modifier_cooldown avec la première fixture."""
    son = Son_Aleatoire(**son_aleatoire1_kwargs)
    son.modifier_cooldown_min(3)
    assert son.cooldown_min == 3


def test_modifier_cooldown_max(son_aleatoire1_kwargs):
    """Test de la méthode modifier_cooldown avec la première fixture."""
    son = Son_Aleatoire(**son_aleatoire1_kwargs)
    son.modifier_cooldown_max(8)
    assert son.cooldown_max == 8


# Test pour vérifier le type des cooldowns lors de l'initialisation
def test_initialisation_cooldown_type_int(son_aleatoire1_kwargs):
    son = Son_Aleatoire(**son_aleatoire1_kwargs)
    assert isinstance(son.cooldown_min, int)
    assert isinstance(son.cooldown_max, int)


# def test_jouer_son_aléatoire():
# pass
