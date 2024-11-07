import pytest
from business_object.son_aleatoire import Son_Aleatoire


def test_initialisation_son_aleatoire(son_aleatoire1_kwargs):
    """Test de l'initialisation de Son_Aleatoire avec la première fixture."""
    son = Son_Aleatoire(**son_aleatoire1_kwargs)

    assert son.nom == "Ambiance de forêt"
    assert son.description == "Son de fond de forêt calme"
    assert son.duree == 60
    assert son.id_freesound == "787956"
    assert son.tags == ["nature", "calm", "forest"]
    assert son.cooldown_min == 5
    assert son.cooldown_max == 10


def test_modifier_cooldown(son_aleatoire1_kwargs):
    """Test de la méthode modifier_cooldown avec la première fixture."""
    son = Son_Aleatoire(**son_aleatoire1_kwargs)
    son.modifier_cooldown(3, 8)
    assert son.cooldown_min == 3
    assert son.cooldown_max == 8


# Test pour vérifier le type des cooldowns lors de l'initialisation
def test_initialisation_cooldown_type_int(son_aleatoire1_kwargs):
    son = Son_Aleatoire(**son_aleatoire1_kwargs)
    assert isinstance(son.cooldown_min, int)
    assert isinstance(son.cooldown_max, int)


# Tests pour vérifier les erreurs de type et de valeur
@pytest.mark.parametrize(
    "cooldown_min, cooldown_max, expected_exception, expected_message",
    [
        ("5", 10, TypeError, "Les cooldowns doivent être des entiers."),
        (5, "10", TypeError, "Les cooldowns doivent être des entiers."),
        (-1, 10, ValueError, "Les cooldowns ne peuvent pas être négatifs."),
        (5, -1, ValueError, "Les cooldowns ne peuvent pas être négatifs."),
        (15, 10, ValueError, "Le cooldown minimum ne peut pas être supérieur au cooldown maximum."),
    ],
)
def test_initialisation_cooldown_exceptions(
    cooldown_min, cooldown_max, expected_exception, expected_message
):
    with pytest.raises(expected_exception, match=expected_message):
        Son_Aleatoire("Nom", "Description", 60, "787956", ["tag"], cooldown_min, cooldown_max)


# Test pour vérifier les erreurs de type lors de la modification des cooldowns
@pytest.mark.parametrize(
    "new_cooldown_min, new_cooldown_max, expected_exception, expected_message",
    [
        ("3", 15, TypeError, "Les cooldowns doivent être des entiers."),
        (3, "15", TypeError, "Les cooldowns doivent être des entiers."),
        (-1, 15, ValueError, "Les cooldowns ne peuvent pas être négatifs."),
        (3, -1, ValueError, "Les cooldowns ne peuvent pas être négatifs."),
        (15, 10, ValueError, "Le cooldown minimum ne peut pas être supérieur au cooldown maximum."),
    ],
)
def test_modifier_cooldown_exceptions(
    son_aleatoire1_kwargs, new_cooldown_min, new_cooldown_max, expected_exception, expected_message
):
    son = Son_Aleatoire(**son_aleatoire1_kwargs)
    with pytest.raises(expected_exception, match=expected_message):
        son.modifier_cooldown(new_cooldown_min, new_cooldown_max)


def test_modifier_cooldown_no_change_on_error(son_aleatoire1_kwargs):
    """Test que les cooldowns ne changent pas en cas d'erreur dans modifier_cooldown."""
    son = Son_Aleatoire(**son_aleatoire1_kwargs)
    original_cooldown_min = son.cooldown_min
    original_cooldown_max = son.cooldown_max

    with pytest.raises(ValueError):
        son.modifier_cooldown(15, 10)  # Cela devrait lever une exception

    assert son.cooldown_min == original_cooldown_min
    assert son.cooldown_max == original_cooldown_max


# def test_jouer_son_aléatoire():
# pass
