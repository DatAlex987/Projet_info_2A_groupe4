"""Ce module implémente la classe abstraite AbstractView"""

from abc import ABC, abstractmethod


class AbstractView(ABC):
    """Classe abstraite définissant la structure des views"""

    def __init__(self):
        self.style = {
            "separator": "ffffff",
            "questionmark": "000000",
            "selected": "00BFFF",
            "pointer": "ffffff",
            "instruction": "ffffff",
            "answer": "008000",
            "question": "FF7F50",
        }

    @abstractmethod
    def display_info(self):
        """Affiche un bandeau information"""
        pass

    @abstractmethod
    def make_choice(self, session):
        """Regroupe les interactions avec l'utilisateur

        Parameters
        -------------------
        user_info : Client / str
            Permet de récupérer les informations de l'utilisateur de views en views
        """
        pass


# Utiliser singleton session
