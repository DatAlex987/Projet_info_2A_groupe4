from unittest.mock import MagicMock
import pytest
import re
from src.service.freesound import Freesound


@pytest.mark.parametrize(
    "tag, limit, expected_error, error_type",
    [
        (["wind"], 15, "L'argument tag n'est pas un str.", TypeError),
        ("wind", -4, "L'argument limit ne peut pas être négatif.", ValueError),
        ("wind", "15", "L'argument limit n'est pas un int.", TypeError),
    ],
)
def test_rechercher_par_tag_echec(tag, limit, expected_error, error_type):
    with pytest.raises(error_type, match=re.escape(expected_error)):
        Freesound.rechercher_par_tag(tag, limit)


@pytest.mark.parametrize(
    "dico_filtres, limit, expected_error, error_type",
    [
        ("dico", 15, "L'argument dico_filtres n'est pas un dict.", TypeError),
        ({"wind"}, -4, "L'argument limit ne peut pas être négatif.", ValueError),
        ({"wind"}, "15", "L'argument limit n'est pas un int.", TypeError),
    ],
)
def test_rechercher_multi_filtres_echec(dico_filtres, limit, expected_error, error_type):
    with pytest.raises(error_type, match=re.escape(expected_error)):
        Freesound.rechercher_multi_filtres(dico_filtres, limit)
