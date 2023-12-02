import pandas as pd
import json
import bs4
import re 

# Charger le fichier JSON
with open('test.json', 'r', encoding='utf-8') as file:
    json = json.load(file)

def suppressiondelurl(types):
    #certains ingrédients sont accompagnés d'un url que l'on souhaite supprimer dans la chaine de caractères
    if types.startswith('<p>de <a href=') or types.startswith('<p><a href='):
        
        # Extraire la partie entre les balises '<a>' et '</a>'
        partie_extraite = types.split('">')[1].split('</a>')[0]
        
        # Remplacer les éventuels <p> dans la partie extraite
        types = partie_extraite.replace('<p>', '').replace('</p>', '')
    return types
                        
def separation_quantite_ingr(types) :
    #parfois certains ingrédients n'ont pas de quantité associée mais son de la forme : 2 tranches de citron
    #cette fonction sert à séparer le '2 tranches' (quantité) et le 'citron' (ingrédient) en coupant en 2 la chaine de caractère
    # Supprimer le '<p>' de la partie extraite
    quantite = ""
    resultat = types.split(" d’", 1)
    if len(resultat)!=2:
        resultat = types.split(" d'", 1)
    if len(resultat)!=2:
        resultat = types.split(" de", 1)        
    if len(resultat)==2: 
        resultat[0] = resultat[0].replace('<p>', '')
        resultat[1] = resultat[1].replace('</p>\n', '')
        types = resultat[1]
    # Placer cette partie dans le deuxième élément de la sous-liste
        quantite = resultat[0]

    # Enlever cette partie de la liste des ingrédients
    return (types, quantite)
        
def nettoyage(num_cocktail):
    liste=[]
    for result in json.get('results', []):  #on rentre dans la catégorie "result"    
        for hit in result.get('hits', []):  #on rentre dans la catégorie "hit" (chaque hit correspond à un cocktail)         
            ingredients = []
            quantites = []
            cocktail = []

            if 'ingredients' in hit: #on cheche s'il y a des ingrédients du type 'ingredients' dans chaque cocktail
                for ingredient in hit['ingredients']:
                    
                    label = ingredient['label'] #certains ingrédients sont sous forme de label
                    ingr = ingredient['ingredient'] #d'autres sous forme d'ingredient
                    quantite = ingredient['quantity'] #quantité associée à chaque label/ingredient
                    
                    label = suppressiondelurl(label)
                    ingr = suppressiondelurl(ingr)
                    #quantite = suppressiondelurl(quantite)

                    if label != "" :
                        label = label.replace("</span>", "")
                        label2 = label
                        if label.startswith('<p>') and any(char.isdigit() for char in label.split('<p>', 1)[-1]):
                            label2 = separation_quantite_ingr(label)[0]
                            quantite = separation_quantite_ingr(label)[1]
                        ingredients.append(label2)
                        quantites.append(quantite)

                  
                    if ingr != "" :
                        ingr = ingr.replace("</span>", "")
                        ingr2 = ingr
                        
                        if ingr.startswith('<p>') and any(char.isdigit() for char in ingr.split('<p>', 1)[-1]):
                            ingr2 = separation_quantite_ingr(ingr)[0]
                            quantite = separation_quantite_ingr(ingr)[1]

                        ingredients.append(ingr2)
                        quantites.append(quantite)
                    #print(ingredients)

                    for i in range (len(ingredients)):
                        element = ingredients[i]
                        
                        # Utiliser une expression régulière pour extraire le texte entre > et <
                    
                        if element.startswith('de '):
                            element = element[3:]
                            ingredients[i]=element
                        elif element.startswith('de'):
                            element = element[2:]
                            ingredients[i]=element
                        elif element.startswith("d'"):
                            element = element[2:]
                            ingredients[i]=element
                        elif element.startswith("<p>d’"):
                            element = element[5:]
                        elif element.startswith('<p>de '):
                            element = element[6:]
                            ingredients[i]=element
                        elif element.startswith('<p>'):
                            element = element[3:]
                            ingredients[i]=element
                        if element.endswith('</p>\n'):
                            element = element[:-5]
                            ingredients[i]=element
                        
                        
                cocktail.append(ingredients)
                cocktail.append(quantites)
                liste.append(cocktail)

    # Afficher le résultat
    return (liste[num_cocktail])
for i in range (120,130):
    print(nettoyage(i))



