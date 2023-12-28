import pandas as pd
from rapidfuzz import process, fuzz
import re

# Charger la colonne de référence (première colonne de test33.xlsx) et la nommer 'Référence'
df_reference = pd.read_excel("/home/onyxia/work/Projet-python-2.0/main/test33.xlsx", usecols=[0])
df_reference.columns = ['Référence']

# Ajouter une ligne vide au début de df_reference pour l'alignement
df_reference = pd.concat([pd.DataFrame([{'Référence': None}]), df_reference]).reset_index(drop=True)

def nettoyer_pour_comparaison(texte):
    return re.sub(r'[^\w\s]', '', texte)

def supprimer_mot_si_correspondance(ingredient, mots_reference, score_minimum=83):
    modifications = 0
    for mot in mots_reference:
        mot_nettoyé = nettoyer_pour_comparaison(mot)
        ingredient_nettoyé = nettoyer_pour_comparaison(ingredient)
        meilleur_match = process.extractOne(mot_nettoyé, [ingredient_nettoyé], scorer=fuzz.WRatio)
        if meilleur_match and meilleur_match[1] > score_minimum:
            pattern = re.escape(mot)
            ingredient, nombre_substitutions = re.subn(pattern, '', ingredient)
            modifications += nombre_substitutions
    return ingredient.strip(), modifications

def filtrer_ingredients(fichier_ingredients, fichier_mots_reference, fichier_sortie):
    df_ingredients = pd.read_excel(fichier_ingredients, header=None, names=['Ingredient'])
    df_ingredients.reset_index(drop=True, inplace=True)  # Réinitialiser l'index
    
    df_ingredients = pd.concat([df_reference, df_ingredients], axis=1)
    df_mots_reference = pd.read_excel(fichier_mots_reference, header=None, names=['Mot'])
    mots_reference = set(df_mots_reference['Mot'].str.lower())

    total_modifications = 0
    for i, row in df_ingredients.iterrows():
        ingredient_nettoyé, modifications = supprimer_mot_si_correspondance(row['Ingredient'].lower(), mots_reference)
        df_ingredients.at[i, 'Ingredient'] = ingredient_nettoyé
        total_modifications += modifications

    df_ingredients.to_excel(fichier_sortie, index=False)
    return total_modifications

# Utilisation
nombre_modifications = filtrer_ingredients(
    "/home/onyxia/work/Projet-python-2.0/main/test33.xlsx",
    "/home/onyxia/work/Projet-python-2.0/main/qtité.xlsx",
    "/home/onyxia/work/Projet-python-2.0/main/test202.xlsx"
)
print(f"Nombre total de suppressions effectuées : {nombre_modifications}")

import pandas as pd
from rapidfuzz import process, fuzz

def charger_mots_reference(chemin_fichier_mots):
    with open(chemin_fichier_mots, 'r', encoding='utf-8') as file:
        mots_reference = [ligne.strip() for ligne in file]
    return set(mots_reference)

def filtrer_ingredients(chemin_fichier_ingredients, chemin_fichier_mots_reference, chemin_fichier_sortie, chemin_fichier_reference):
    # Charger les ingrédients et la colonne de référence
    df_ingredients = pd.read_excel(chemin_fichier_ingredients, header=None, names=['Ingredient'])
    df_reference = pd.read_excel(chemin_fichier_reference, usecols=[0])
    df_reference.columns = ['Référence']
    
    # Vérifier que le nombre de lignes est identique
    if len(df_ingredients) != len(df_reference):
        raise ValueError("Le nombre de lignes dans le fichier des ingrédients et la référence ne correspond pas.")
    
    # Fusionner les DataFrames sur l'index pour garder la référence associée à chaque ingrédient
    df_ingredients = pd.concat([df_reference, df_ingredients], axis=1)
    
    mots_reference = charger_mots_reference(chemin_fichier_mots_reference)
    
    # Filtrer les ingrédients
    ingredients_filtres = []
    for index, row in df_ingredients.iterrows():
        ingr = row['Ingredient']
        if isinstance(ingr, str):
            mots_ingr = [mot.lower() for mot in ingr.split() if mot.isalpha()]  # Exclure les caractères spéciaux
            mots_ingr_filtres = [mot for mot in mots_ingr if mot in mots_reference]
            if mots_ingr_filtres:
                ingredients_filtres.append({'Référence': row['Référence'], 'Ingredient': ' '.join(mots_ingr_filtres)})
    
    # Créer un nouveau DataFrame avec les ingrédients filtrés et leur référence
    df_resultat = pd.DataFrame(ingredients_filtres)
    
    # Enregistrer le résultat dans un nouveau fichier Excel
    df_resultat.to_excel(chemin_fichier_sortie, index=False)

# Exemple d'utilisation
filtrer_ingredients(
    "/home/onyxia/work/Projet-python-2.0/main/test202 copy.xlsx",
    "/home/onyxia/work/Projet-python-2.0/main/mot dico.txt",
    "/home/onyxia/work/Projet-python-2.0/main/test2012.xlsx",
    "/home/onyxia/work/Projet-python-2.0/main/test202 copy.xlsx"  # Chemin du fichier de référence
)
