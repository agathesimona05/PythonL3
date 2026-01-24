import pandas as pd

print(pd.__version__)


data = {
    "Nom": ["Alice", "Bob", "Charlie"],
    "Age": [20, 22, 19],
    "Note": [14.5, 16, 12]
}

df = pd.DataFrame(data)
print(df)

import pandas as pd

# Création d'un petit tableau de données
data = {
    "Nom": ["Alice", "Bob", "Charlie", "Dina"],
    "Note": [12, 15, 9, 17]
}

df = pd.DataFrame(data)

print("Tableau de données :")
print(df)

print("\nMoyenne des notes :", df["Note"].mean())
print("Note maximale :", df["Note"].max())
print("Note minimale :", df["Note"].min())

print("\nÉtudiants admis (note >= 10) :")
print(df[df["Note"] >= 10])