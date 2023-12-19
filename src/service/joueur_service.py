from tabulate import tabulate

from utils.log_decorator import log

from dto.joueur import Joueur
from dao.joueur_dao import JoueurDao


class JoueurService:
    @log
    def creer(self, pseudo, mdp, age, mail, fan_pokemon) -> Joueur:
        """Création d'un joueur"""

        nouveau_joueur = Joueur(
            pseudo=pseudo, mdp=mdp, age=age, mail=mail, fan_pokemon=fan_pokemon
        )

        return nouveau_joueur if JoueurDao().creer(nouveau_joueur) else None

    @log
    def lister_tous(self) -> list[Joueur]:
        """Lister tous les joueurs"""
        return JoueurDao().lister_tous()

    @log
    def trouver_par_id(self, id_joueur) -> Joueur:
        """Trouver un joueur à partir de son id"""
        return JoueurDao().trouver_par_id(id_joueur)

    @log
    def supprimer(self, joueur) -> bool:
        """Supprimer le compte d'un joueur"""
        return JoueurDao().supprimer(joueur)

    @log
    def afficher_tous(self) -> str:
        """Afficher tous les joueurs
        Sortie : Une chaine de caractères mise sous forme de tableau
        """
        entetes = ["pseudo", "age", "mail", "est fan de Pokemon"]

        joueurs = JoueurDao().lister_tous()
        joueurs_as_list = [j.as_list() for j in joueurs]

        str_joueurs = "-" * 100
        str_joueurs += "\nListe des joueurs \n"
        str_joueurs += "-" * 100
        str_joueurs += "\n"
        str_joueurs += tabulate(
            tabular_data=joueurs_as_list,
            headers=entetes,
            tablefmt="psql",
            floatfmt=".2f",
        )
        str_joueurs += "\n"

        return str_joueurs

    @log
    def se_connecter(self, pseudo, mdp) -> Joueur:
        """Se connecter à partir de pseudo et mdp"""
        joueur = JoueurDao().se_connecter(pseudo, mdp)
        if not joueur:
            print(f"Connexion {pseudo} refusée")
        else:
            print(f"Joueur {joueur.pseudo} connecté")
        print("*" * 100)
        return joueur

    @log
    def pseudo_deja_utulise(self, pseudo) -> bool:
        """Vérifie si le pseudo est déjà utilisé
        Retourne True si le pseudo existe déjà en BDD"""
        joueurs = JoueurDao().lister_tous()
        return pseudo in [j.pseudo for j in joueurs]