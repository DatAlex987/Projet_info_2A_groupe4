import pygame
import threading
import datetime
import sys
import time
from src.business_object.son_continu import Son_Continu
from src.business_object.son_manuel import Son_Manuel

# Initialisation de pygame

pygame.mixer.init()

# Chargement du son (remplacez 'son.wav' par le chemin de votre fichier son)

son = Son_Manuel(
    nom="The Imperial March",
    description="Luke, I am your father",
    duree=datetime.timedelta(seconds=45),
    id_freesound="662970",
    tags=["starwars", "Vador", "JW"],
    start_key="j",
)

son.jouer_son()
