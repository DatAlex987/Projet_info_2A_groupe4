# Projet_info_2A_groupe4

Application The DM's Sound Buddy.
Membres du groupe :
- LAO Alex
- BOCQUET Noémie
- BOUZERIA Wissal
- SECK El Hadji Massamba
- SANNIER Théo

## :arrow_forward: Logiciels requis

- [Visual Studio Code](https://code.visualstudio.com/)
- [Python 3.10](https://www.python.org/)
- [Git](https://git-scm.com/)
- Une base de données [PostgreSQL](https://www.postgresql.org/)

---

## :arrow_forward: Installez les packages nécessaires

Dans VSCode :
```bash
pip install -r requirements.txt
pip list
```

---

## :arrow_forward: Variables d'environnement

L'application requiere les variables d'environnement ci-dessous pour fonctionner :
À la racine du projet le fichier :

```default
POSTGRES_HOST = X
POSTGRES_PORT = 5432
POSTGRES_DATABASE = X
POSTGRES_USER = X
POSTGRES_PASSWORD = X
POSTGRES_SCHEMA = ProjetInfo


API_KEY = X
CLIENT_ID = X
URL_API = https://freesound.org/apiv2/
DOSSIER_SAUVEGARDE = P:\...\Fichiers_audio_téléchargés
```

---

## :arrow_forward: Lancer les tests unitaires

Pour le lancement des tests :

```bash
python -m pytest src/tests
```

## :arrow_forward: Lancer le programme

Cette application propose une interface dans le terminal, ainsi qu'avec une fenêtre PyGame.

Pour profiter d'une base de données déjà peuplée, lancez le script `reset_database.py`
L'utilisateur suivant est d'ores et déjà doté de multiples créations :

Nom : De Vannes
Prénom : Karadoc
Pseudo : KaradocDV
Mot de Passe : Kdv1234@

Vous pouvez vous y connecter.
Un autre utilisateur (pseudo: PercevalDG) possède une sound-deck JDR Versaillais

Puis, pour lancer l'application, lancez le script `src/__main__.py`

---

