
import pandas as pd
from rapidfuzz import process, fuzz


# Charger les données des deux feuilles Excel
df1 = pd.read_excel("/home/onyxia/work/Projet-python-2.0/main/test3.xlsx")
df2 = pd.read_excel("/home/onyxia/work/Projet-python-2.0/main/Cocktails - Ref - Ingrédients.xlsx")


# Utiliser la première et la deuxième colonne pour chaque DataFrame
col_ingredient_df1 = df1.columns[0]
col_mot_df1 = df1.columns[1]
col_ingredient_df2 = df2.columns[0]
col_mot_df2 = df2.columns[1]

# Fonction pour trouver la meilleure correspondance avec rapidfuzz
def trouver_correspondance(ingredient, df_ref, seuil=88):
    correspondances = process.extractOne(ingredient, df_ref[col_ingredient_df2], scorer=fuzz.WRatio)
    if correspondances and correspondances[1] >= seuil:
        return correspondances[0]
    return None

# Associer les mots
resultats = []
for _, row in df1.iterrows():
    correspondance = trouver_correspondance(row[col_ingredient_df1], df2)
    if correspondance:
        mot_associe = df2[df2[col_ingredient_df2] == correspondance][col_mot_df2].iloc[0]
    else:
        mot_associe = row[col_mot_df1]
    resultats.append({col_ingredient_df1: row[col_ingredient_df1], 'Mot_Associe': mot_associe})

# Créer un nouveau DataFrame
df_resultat = pd.DataFrame(resultats)


# Exporter en Excel
df_resultat.to_excel("/home/onyxia/work/Projet-python-2.0/main/testcomparaisonavecref.xlsx", index=False)
