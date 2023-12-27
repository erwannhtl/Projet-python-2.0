import pandas as pd
from rapidfuzz import process, fuzz
import concurrent.futures

def nettoyer_texte(texte):
    return ''.join(e for e in texte if e.isalnum()).lower()

def extraire_premier_mot(texte):
    return texte.split()[0] if texte and texte.split() else texte

def fuzzy_matching(ingredient, ingredient_list, score_minimum=85):  # Réduire un peu le score minimum
    matches = process.extract(ingredient, ingredient_list, scorer=fuzz.WRatio, limit=None)
    best_match = (None, 0)
    for match in matches:
        # Pondération supplémentaire si le premier mot correspond
        adjusted_score = match[1]
        if extraire_premier_mot(ingredient) == extraire_premier_mot(match[0]):
            adjusted_score += 5  # Ajouter un bonus pour les correspondances du premier mot

        if adjusted_score > best_match[1]:
            best_match = (match[0], adjusted_score)

    return best_match if best_match[1] > score_minimum else (None, 0)


def faire_correspondance(fichier_excel1, fichier_excel2, colonne1, colonne2, sortie, score_minimum=87):
    df1 = pd.read_excel(fichier_excel1, header=None, names=[colonne1])
    df2 = pd.read_excel(fichier_excel2, header=None, names=[colonne2])

    df1['Nettoyé'] = df1[colonne1].apply(nettoyer_texte)
    df2['Nettoyé'] = df2[colonne2].apply(nettoyer_texte)
    ingredient_list2 = df2['Nettoyé'].tolist()

    correspondances = [fuzzy_matching(ingredient, ingredient_list2, score_minimum) for ingredient in df1['Nettoyé']]

    # Création des colonnes pour les correspondances et les scores
    df1['Correspondance'] = [None] * len(df1)
    df1['Score'] = [0] * len(df1)
    
    for i, match in enumerate(correspondances):
        if match[0]:  # Vérifiez si match[0] n'est pas None
            index_match = ingredient_list2.index(match[0])
            df1.at[i, 'Correspondance'] = df2[colonne2].iloc[index_match]
            df1.at[i, 'Score'] = match[1]

    # Filtrer les lignes avec un score supérieur au score minimum
    df1_filtré = df1[df1['Score'] > score_minimum]
    nombre_associes = df1_filtré['Correspondance'].count()

    df1.to_excel(sortie, index=False, columns=[colonne1, 'Correspondance', 'Score'])

    return nombre_associes

# Exemple d'utilisation
# Vous pouvez spécifier un mot clé si nécessaire, par exemple 'sirop' ou le laisser à None pour utiliser le premier mot.
nombre_associes = faire_correspondance("/home/onyxia/work/Projet-python-2.0/main/test11.xlsx", "/home/onyxia/work/Projet-python-2.0/main/tes22.xlsx", "Ingrédients1", "Ingrédients2", "/home/onyxia/work/Projet-python-2.0/main/test3.xlsx", score_minimum=70)
print(f"Nombre d'ingrédients associés avec un score supérieur à {70}: {nombre_associes}")



# Exemple d'utilisation
