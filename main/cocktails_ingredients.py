#BUT : nettoyer le fichier cocktails_ingrédients afin d'obtenir une base simplifiée liant les cocktails aux ingrédients simplifiés 

import pandas as pd
from fuzzywuzzy import fuzz
import os

os.chdir('main')

cocktails_ingredients = pd.read_csv('../main/aliments_selection.csv')
print(cocktails_ingredients.head())

#séparer alcools et ingrédients - Même liste que dans le fichier cocktail.py
base_alcool = ['Gin', 'Vodka', 'Rhum','Liqueur','Tequila','Vin','Whisky','Vermouth','Crème', 'Amaretto', 'Bière', 'Cidre', 'Cognac', 'Limoncello', 'Eau-de-vie','Mezcal','Acerum','Brandy'] 

for i in range(len(cocktails_ingredients['Nom'])):
    aliment = cocktails_ingredients.at[i, 'Nom']
    for alcool in base_alcool:
        ratio = fuzz.token_set_ratio(aliment, alcool)
        if ratio > 95:
            cocktails_ingredients.at[i, 'Nom'] = alcool


print(cocktails_ingredients.head())

# Enregistrer le DataFrame modifié dans le même fichier CSV
cocktails_ingredients.to_csv('aliments_selection.csv', index=False)

