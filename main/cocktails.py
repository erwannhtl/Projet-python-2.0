import json
import os

# Imprimer le chemin absolu du fichier JSON
json_file_path = os.path.abspath('data.json')
print(f"Chemin absolu du fichier JSON : {json_file_path}")

# Charger les données JSON depuis le fichier
with open(json_file_path, 'r') as file:
    data = json.load(file)

from bs4 import BeautifulSoup

# Initialiser le dictionnaire
cocktails_dict = {}

# Itérer sur les cocktails,
#boucle for qui itère au sein du premier élément du dictionnairesur chaque élément de la liste hits et utilise la variable hit pour représenter chaque élément successif à chaque itération.
for hit in data['results'][0]['hits']:
    cocktail_name = hit['post_title']
    cocktail_recipe = hit['content']
    cocktail_url = hit['url']
    cocktail_ingredients = []

    # Vérifier si la clé 'ingredients' est présente
    if 'ingredients' in hit:
        # Itérer sur les ingrédients
        for ingredient in hit['ingredients']:
            if ingredient['type'] == 'ingredient' and ingredient['ingredient']:
                # Utiliser BeautifulSoup pour extraire le texte de l'élément HTML
                ingredient_text = BeautifulSoup(ingredient['ingredient'], 'html.parser').get_text()
                
                # Ajouter les ingrédients non vides
                cocktail_ingredients.append(ingredient_text)

    # Ajouter les informations au dictionnaire
    cocktails_dict[cocktail_name] = {
        'recipe': cocktail_recipe,
        'url': cocktail_url,
        'ingredients': cocktail_ingredients
    }

# Afficher le dictionnaire
#print(cocktails_dict)

# Afficher les deux premières lignes du dictionnaire
for index, (cocktail_name, cocktail_info) in enumerate(cocktails_dict.items()):
    print(f"{index + 1}. {cocktail_name}:")
    print(f"   Recette : {cocktail_info['recipe']}")
    print(f"   URL : {cocktail_info['url']}")
    print(f"   Ingrédients : {cocktail_info['ingredients']}")
    print("\n")

    # S'arrêter après deux itérations
    if index == 1:
        break
