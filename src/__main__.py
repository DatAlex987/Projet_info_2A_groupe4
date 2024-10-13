from dao.user_dao import UserDAO
from utils.reset_database import ResetDatabase

ResetDatabase().lancer()
print(
    UserDAO.ajouter_user(
        pseudo="swannetneo",
        mdp_hashe="mdp123",
        age=99,
        nom="swann",
        prenom="neo",
    )
)
