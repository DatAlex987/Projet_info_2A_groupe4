import pygame
import threading
import datetime
import sys
import time
from src.business_object.son_continu import Son_Continu
from src.business_object.son_manuel import Son_Manuel
from src.business_object.son_aleatoire import Son_Aleatoire

# Initialisation de pygame

pygame.mixer.init()

# Chargement du son (remplacez 'son.wav' par le chemin de votre fichier son)

son = Son_Aleatoire(
    nom="Manoir hanté",
    description="Son de fantome dans un manoir",
    duree=datetime.timedelta(seconds=30),
    id_freesound="662970",
    tags=["manoir", "fantome", "scary"],
    cooldown_min=3,
    cooldown_max=6,
)

son2 = Son_Manuel(
    nom="Manoir hanté",
    description="Son de fantome dans un manoir",
    duree=datetime.timedelta(seconds=30),
    id_freesound="662970",
    tags=["manoir", "fantome", "scary"],
    start_key="j",
)

son2.jouer_son()
