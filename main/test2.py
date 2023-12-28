import pandas as pd
from rapidfuzz import process, fuzz
import re

  


def nettoyer_pour_comparaison(texte):
    # Supprimer les caractères spéciaux et les parenthèses pour la comparaison
    return re.sub(r'[^\w\s]', '', texte)

def supprimer_mot_si_correspondance(ingredient, mots_reference, score_minimum=3):
    modifications = 0
    ingredient_original = ingredient
    for mot in mots_reference:
        # Nettoyer le mot et l'ingrédient pour la comparaison
        mot_nettoyé = nettoyer_pour_comparaison(mot)
        ingredient_nettoyé = nettoyer_pour_comparaison(ingredient)
        meilleur_match = process.extractOne(mot_nettoyé, [ingredient_nettoyé], scorer=fuzz.WRatio)
        if meilleur_match and meilleur_match[1] > score_minimum:
            pattern = re.escape(mot)  # Échapper les caractères spéciaux pour les regex
            ingredient, nombre_substitutions = re.subn(pattern, '', ingredient)
            modifications += nombre_substitutions
    return ingredient.strip(), modifications  # Retourner l'ingrédient nettoyé et le nombre de suppressions

def filtrer_ingredients(fichier_ingredients, fichier_mots_reference, fichier_sortie):
    df_ingredients = pd.read_excel(fichier_ingredients, header=None, names=['Ingredient'])
    df_mots_reference = pd.read_excel(fichier_mots_reference, header=None, names=['Mot'])

    mots_reference = set(df_mots_reference['Mot'].str.lower())

    total_modifications = 0
    # Utiliser items() au lieu de iteritems()
    for i, ingredient in df_ingredients['Ingredient'].items():
        ingredient_nettoyé, modifications = supprimer_mot_si_correspondance(ingredient.lower(), mots_reference)
        df_ingredients.at[i, 'Ingredient'] = ingredient_nettoyé
        total_modifications += modifications

    df_ingredients.to_excel(fichier_sortie, index=False)

    return total_modifications

# Exemple d'utilisation
nombre_modifications = filtrer_ingredients(
    "/home/onyxia/work/Projet-python-2.0/main/test33.xlsx",
    "/home/onyxia/work/Projet-python-2.0/main/qtité.xlsx",
    "/home/onyxia/work/Projet-python-2.0/main/test202.xlsx"
)
print(f"Nombre total de suppressions effectuées : {nombre_modifications}")

######### Partie 1

import pandas as pd
from rapidfuzz import process, fuzz

with open("/home/onyxia/work/Projet-python-2.0/main/mot dico.txt", "r", encoding="utf-8") as fichier:
    contenu = fichier.read()

def charger_mots_reference(chemin_fichier_mots):
    with open(chemin_fichier_mots, 'r') as file:
        mots_reference = [ligne.strip() for ligne in file]
    return set(mots_reference)

def filtrer_ingredients(chemin_fichier_ingredients, chemin_fichier_mots_reference, chemin_fichier_sortie):
    df_ingredients = pd.read_excel(chemin_fichier_ingredients, header=None, names=['Ingredient'])
    mots_reference = charger_mots_reference(chemin_fichier_mots_reference)

    # Diviser chaque ingrédient en mots et comparer avec les mots du dictionnaire
    ingredients_filtres = []

    for ingr in df_ingredients['Ingredient']:
        if isinstance(ingr, str):
            mots_ingr = [mot.lower() for mot in ingr.split() if mot.isalpha()]  # Exclure les caractères spéciaux
            mots_ingr_filtres = [mot for mot in mots_ingr if mot in mots_reference]

            if mots_ingr_filtres:
                ingredients_filtres.append(' '.join(mots_ingr_filtres))

    # Créer un nouveau DataFrame avec les ingrédients filtrés
    df_resultat = pd.DataFrame({'Ingredient': ingredients_filtres})

    # Enregistrer le résultat dans un nouveau fichier Excel
    df_resultat.to_excel(chemin_fichier_sortie, index=False)



# Exemple d'utilisation
filtrer_ingredients(
    "/home/onyxia/work/Projet-python-2.0/main/test202.xlsx",
    "/home/onyxia/work/Projet-python-2.0/main/mot dico.txt",
    "/home/onyxia/work/Projet-python-2.0/main/test2012.xlsx"
)








#Partie 2
##############################################################################################
import pandas as pd
from rapidfuzz import process, fuzz
import re

def nettoyer_pour_clé(texte):
    # Convertir tout non-chaîne en chaîne
    texte = str(texte)
    # Supprimer les caractères spéciaux et les espaces superflus
    return re.sub(r'[^\w\s]', '', texte).strip()

# La fonction 'fusionner_ingredients_exigeants' et 'calculer_score_avec_poids' restent les mêmes
# ...



# Fonction pour calculer le score avec un poids supplémentaire sur le premier mot
def calculer_score_avec_poids(ingredient, autre_ingredient):
    # Donner plus de poids au premier mot
    poids_premier_mot = 2.0
    score_total = 0.0

    mots_ingredient = ingredient.split()
    mots_autre_ingredient = autre_ingredient.split()

    if mots_ingredient and mots_autre_ingredient:
        # Calculer le score pour le premier mot avec un poids supplémentaire
        score_total += fuzz.WRatio(mots_ingredient[0], mots_autre_ingredient[0]) * poids_premier_mot

        # Calculer le score pour les autres mots
        for mot in mots_ingredient[1:]:
            score_mot = max(fuzz.WRatio(mot, mot_autre) for mot_autre in mots_autre_ingredient)
            score_total += score_mot

        # Normaliser le score
        score_total /= (poids_premier_mot + len(mots_ingredient) - 1)

    return score_total

# La fonction 'fusionner_ingredients_exigeants' reste la même que précédemment
# ...
def fusionner_ingredients_exigeants(df, score_seuil=85):
    ingredients = df['Ingredient'].tolist()
    ingredients_fusionnes = {}
    nombre_fusions = 0

    for ingredient in ingredients:
        ingredient_nettoye = nettoyer_pour_clé(ingredient)

        meilleur_match, score = None, 0
        for autre_ingredient in ingredients_fusionnes.keys():
            score_temp = calculer_score_avec_poids(ingredient_nettoye, autre_ingredient)
            if score_temp > score:
                score = score_temp
                meilleur_match = autre_ingredient

        if meilleur_match and score >= score_seuil:
            if len(ingredient_nettoye) <= len(meilleur_match):
                ingredients_fusionnes[ingredient_nettoye] = ingredients_fusionnes.pop(meilleur_match)
                ingredients_fusionnes[ingredient_nettoye].append(ingredient)
                nombre_fusions += 1
            else:
                ingredients_fusionnes[meilleur_match].append(ingredient)
        else:
            if ingredient_nettoye not in ingredients_fusionnes:
                ingredients_fusionnes[ingredient_nettoye] = [ingredient]

    resultat = []
    for ingr_principal, ingr_similaires in ingredients_fusionnes.items():
        for ingr in ingr_similaires:
            resultat.append({'Ingredient': ingr, 'Fusionné': ingr_principal})

    print(f"Nombre total de fusions effectuées: {nombre_fusions}")
    return pd.DataFrame(resultat)

def creer_excel_fusionnes(df):
    df_fusionnes = df[['Fusionné']].drop_duplicates()
    return df_fusionnes

# Exemple d'utilisation
df_ingredients = pd.read_excel("/home/onyxia/work/Projet-python-2.0/main/test2012.xlsx")
df_resultat = fusionner_ingredients_exigeants(df_ingredients, score_seuil=85)
df_resultat.to_excel("/home/onyxia/work/Projet-python-2.0/main/testfin.xlsx", index=False)
