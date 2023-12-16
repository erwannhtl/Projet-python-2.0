import os
#os.chdir('main')

print('hello world')



import pandas as pd
import json
import bs4
import re 
from fuzzywuzzy import fuzz  #potentiellement à installer

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
    #parfois certains ingrédients n'ont pas de quantité associée mais sont de la forme : 2 tranches de citron
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
#for i in range (380,390):
    print(nettoyage(i))

#print(nettoyage(1))
# l : ici une liste, à modifier pour qu'elle parcoure les alcools de toute la base pour les identifier

liste_alcool = ['gin', 'vodka', 'rhum','liqueur','tequila','vin','whisky','vermouth','sirop','crème', 'amaretto', 'bière', 'cidre', 'cognac', 'limoncello', 'eau-de-vie','mezcal','acerum','brandy'] 
#parcourir la base à la mano pour lister tous les alcools utilisés sans leurs noms propres

#l = nettoyage(1)[0]
#print(l)

def identification_alcool(l):
    # afin d'identifier que 'Gin, Palaiseau' = 'Gin, New York' = 'Gin'
    #nous renvoie une liste avec soit le nom de l'alcool comme dans liste_alcool (donc sans le nom propre), soit erreur
    n = len(l)
    m = len(liste_alcool)
    for j in range(m):
        mot = liste_alcool[j]
        for i in range(n):
            mot_test = l[i]
            ratio = fuzz.token_set_ratio(mot,mot_test)
            if ratio > 95:
                #distance à modifier selon le résultat voulu
                l[i] = mot
            else : 
                l[i] = mot_test
    return l 

#print(identification_alcool(l))


def simplification_ingredients():
    '''Nous renvoie une liste de liste d'ingrédients pour chaque cocktail, avec les alcools simplifiés selon liste_cocktail'''
    ingredients_nettoyes = []
    for i in range(0,390): #390 = nb de cocktails
        a=[]
        l = nettoyage(i)[0]
        a.append(identification_alcool(l))
        a.append(nettoyage(i)[1])
        ingredients_nettoyes.append(a)

    return ingredients_nettoyes


l = simplification_ingredients()

deuxiemes_elements = [element[1] for element in l]

# Écriture dans un fichier texte
with open('fichier.txt', 'w') as fichier:
    for item in deuxiemes_elements:
        fichier.write(str(item) + '\n')



#Afin de pouvoir nettoyer la base Ciqual, on va enlever les doublons de cette liste pour avoir une liste plus simple

def ingredients_sans_doublons():
    '''nous renvoie une liste d'ingrédients unique,sans association aux cocktails'''
    l = simplification_ingredients()
    ingredients_uniques = set()
    for ingr in l :
        ingredients_uniques.update(ingr)
    return list(ingredients_uniques)

#print(ingredients_sans_doublons())


# Vérifier si tous nos alcools sont bien dans la nouvelle liste d'ingrédients unique
#for i in liste_alcool:
    #if i in ingredients_sans_doublons():
        #print('Le',i,'est présent dans la liste d\'ingrédients.')
    #else:
        #print('Le',i,'n\'est pas présent dans la liste d\'ingrédients.')

#print(len(ingredients_sans_doublons()))


