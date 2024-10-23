from unittest.mock import MagicMock, patch
import pytest
from business_object.son_aleatoire import Son_Aleatoire


def test_modifier_cooldown(son_aleatoire1_kwargs):
    test = Son_Aleatoire(**son_aleatoire1_kwargs)
    test.modifier_cooldown(10, 20)
    assert test.cooldown_min == 10 and test.cooldown_max == 20


def jouer_son_aléatoire():
    pass
