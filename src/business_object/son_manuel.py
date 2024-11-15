from business_object.son import Son
import pygame
import threading


class Son_Manuel(Son):
    """
    Classe fille de son qui permet de jouer un son quand on le souhaite à partir d'une touche du
    clavier bien définie


    Attributs
    ----------
    start_key : str
        touche pour lancer le lon

    Examples
    --------
    """

    def __init__(self, nom, description, duree, id_freesound, tags, start_key):
        super().__init__(nom, description, duree, id_freesound, tags)
        self.start_key: str = start_key
        self.charge = None
        if not isinstance(start_key, str):
            raise TypeError("la touche doit être de type String")

    def modifier_key(self, new_key):
        """Modifier la touche pour lancer un son"""
        self.start_key = new_key

    def activation_touche(self):
        input(f"Appuyer sur {self.start_key} pour déclencher le son")
        self.charge.play()

    def Arret_Son(self):
        if self.charge:
            input("Appuyer sur m pour arreter le son manuel")
            self.charge.stop()
            self.charge = None
        else:
            print(f"le son {self.id_freesound} ne joue pas : pygame_error")

    # Thread Worker qui exécute la fonction chaque fois que l'événement est déclenché
    def thread_worker(self, event):
        while True:
            print("En attente du déclenchement...")
            event.wait()  # Attendre que l'événement soit déclenché
            event.clear()  # Réinitialiser l'événement pour pouvoir attendre à nouveau
            self.charge.play()

    def jouer_son(self):
        """lance le son après déclenchement"""
        file_path = self.localise_son()
        # Initialiser Pygame est necessaire :pygame.mixer.init avant
        try:
            self.charge = pygame.mixer.Sound(file_path)
            print("chargé")
            # Run the input listener in a separate thread
            thread_A = threading.Thread(target=self.Arret_Son)
            thread_A.daemon = True  # Ensure it exits when the main program does
            thread_A.start()
            event = threading.Event()
            # Démarrage du thread
            thread_k = threading.Thread(target=self.thread_worker, args=(event,))
            thread_k.daemon = True  # Le thread se termine avec le programme principal
            thread_k.start()
        except pygame.error as e:
            print(f"Erreur lors de la lecture du fichier : {e}")
