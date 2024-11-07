from unittest.mock import MagicMock, patch
import pytest
from business_object.son_manuel import Son_Manuel
from unittest.mock import patch
import pygame


@patch("pygame.event.get")
@patch("pygame.init")
@patch("pygame.quit")
def test_jouer_son_manuel(mock_quit, mock_init, mock_event_get, son_manuel2_kwargs):
    instance = Son_Manuel(**son_manuel2_kwargs)
    instance.JouerSon = MagicMock()  # Simule la méthode JouerSon

    # Simuler le code ASCII de la touche `start_key`
    kpg = ord(instance.start_key)

    # Définir la séquence d'événements de pygame
    # Un événement `KEYDOWN` avec la touche correcte, suivi d'un `QUIT` pour arrêter la boucle
    mock_event_get.side_effect = [
        [pygame.event.Event(pygame.KEYDOWN, {"key": kpg})],
        [pygame.event.Event(pygame.QUIT)],
    ]
    instance.jouer_son_manuel()

    instance.JouerSon.assert_called_once()


def test_modifier_key(son_manuel2_kwargs, son_manuel1_kwargs):
    test1 = Son_Manuel(**son_manuel1_kwargs)
    test1.modifier_key(new_key="0")
    test2 = Son_Manuel(**son_manuel2_kwargs)
    test2.modifier_key(new_key="z")
    assert (test2.start_key == "z") and (test1.start_key == "0")
