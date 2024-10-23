from business_object.user import User
from src.business_object.scene import Scene
from datetime import date


U = User("thierry", "villiers", date(1589, 1, 1), "458749", "mdp", [])
print(type(U))
S = Scene(
    "scenetest",
    "description",
    "598687",
    [],
    [],
    [],
    U,
    date(1999, 1, 1),
)

print(S)
print(S.modifier_nom(12))
