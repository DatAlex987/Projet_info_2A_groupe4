from utils.log_decorator import log
from utils.securite import hash_password
from src.business_object.son import Son
from src.dao.son_dao import SonDAO
import requests
import os
import wget

API_KEY = os.getenv("API_KEY")
dossier_sauvegarde = os.getenv("DOSSIER_SAUVEGARDE")
URL_API = os.getenv("URL_API")


class SonService:
    """méthodes liées aux sons"""

    @log
    def télécharger_son(self, id_son):
        url_sound = f"{URL_API}/sounds/{id_son}/?token={API_KEY}"
        response_sound = requests.get(url_sound)

        if response_sound.status_code == 200:
            sound_data = response_sound.json()
            mp3_url = sound_data["previews"]["preview-hq-mp3"]  # Lien du fichier MP3 haute qualité

            # Télécharger le fichier MP3
            print(f"Téléchargement du son à partir de {mp3_url}")
            mp3_response = requests.get(mp3_url)

            if mp3_response.status_code == 200:
                # Chemin complet vers le fichier dans le dossier Fichiers_audio
                chemin_fichier_mp3 = os.path.join(dossier_sauvegarde, f"{id_son}.mp3")
                with open(chemin_fichier_mp3, "wb") as f:
                    f.write(mp3_response.content)
                print(f"Le fichier a été téléchargé sous le nom {fichier_mp3}")
            else:
                print(f"Erreur lors du téléchargement du fichier : {mp3_response.status_code}")
        else:
            print(
                f"Erreur lors de la récupération des détails du son : {response_sound.status_code}"
            )
