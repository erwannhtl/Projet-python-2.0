# **Projet Python 2A**

Erwann Hotellier • Alexia Duclert • Juliette Schneider

*Ce projet est réalisé dans le cadre du cours de Python de Lino Galiana pour l'année 2023-2024.*

Il s'agit d'un programme qui propose un choix de cocktails optimaux en terme d'apports nutritifs selon le profil et les goûts de la personne.

## Introduction
L'intérêt pour les apports nutritionnels est un sujet de plus en plus prédominant dans notre société consciente de la santé. Alors que la plupart des efforts se concentrent sur les aliments quotidiens et les boissons traditionnelles, ce projet, en se concentrant sur les cocktails, crée un pont entre santé et divertissement. Nous voulions savoir, si les cocktails, souvent associés au plaisir et à la détente, pouvaient néanmoins être source de nutriments.

Nos besoins en nutriments quotidiens varient en fonction de notre âge, de notre sexe, de notre activité physique etc, ainsi, nous souhaitions personnaliser notre projet en fonction des caractéristiques de l'utilisateur : <img src="https://github.com/erwannhtl/Projet-python-2.0/assets/126115377/dd467857-8760-48ee-ac05-8e9b12e8e7d9" width="50%">

Ainsi, notre projet propose une interface à l'utilisateur : il rentre son profil et les ingrédients qu'il souhaite éviter dans son cockail, l'interface lui renvoie plusieurs cocktails, il choisit celui qu'il préfère et l'interface lui affiche les apports nutritifs de ce cocktail par rapport à ses besoins nutritifs journaliers. 

## Présentation des bases de données 

Nous avons travaillé avec trois bases de données : 
- La base des cocktails, data scrappée sur le site 1ou2cocktails
- La base ciqual qui regroupe les données nutritives de plus de 3 000 aliments
- La base DRVs qui nous donnait les apports en nutriments nécessaires en fonction de chaque profil                                        



## Installation et utilisation

Dans le notebook **??** se trouvent les instructions détaillées pour installer les éléments requis et pour utiliser le programme.

## Etape 1 : Scrapping

[1 ou 2 cocktails](" https://1ou2cocktails.com/cocktails/ ")

Nous avons fait data scrappé le site 1ou2cocktails qui nous semblait être le site le plus complet. Cependant, nous ne pouvions pas récupérer les informations dans le code html car certaines parties étaient écrites en Javascript. Nous avons donc fait des requêtes directement au serveur pour récupérer un fichier json avec toutes les informations.

## Etape 2 : Nettoyage des ingrédients et bijection avec Ciqual

Nous détaillons dans le notebook les différentes étapes de nettoyages des ingrédients. Cette étape était assez complexe car nous devions faire l'arbitrage entre précision et simplification. En effet, en travaillant avec de la reconnaissance de texte, par définition imprécise, en voulant trop nettoyer, nous perdions beaucoup d'informations et inversement.

Les ingrédients de la base sont très précis, avec un certains nombres de noms propres, en particulier pour les alcools. Dans la suite du projet, nous souhaitons sélectionner des cocktails par leurs ingrédients, afin de prendre en compte les goûts de l'utilisateur. 

Si la quantité d'ingrédient est dense est très diversifiée, le nombre d'alcool est limité. Nous avons donc décidé de simplifier tous les noms d'alcools de la base en des catégories plus grandes. Par exemple, 'gin de Palaiseau' et 'gin de New-York' deviendront 'gin', toutes les liqueurs différentes seront uniquement dénommées par 'liqueur'.

Pour ce faire, nous avons extrait du site de recette de cocktails les différentes classes d'alcools qu'ils considèrent. Ensuite, nous avons utilisé la **Partial Levenshtein distance (FWZ)**, implémentée par le module `fuzzywuzzy`, qui cacule la distance de Levenshtein entre la chaîne la plus courte et tous les sous-chaînes de la chaîne la plus longue de même longueur que la chaîne la plus courte, et ensuite prend le minimum de toutes ces valeurs. Cette distance nous a permis de comparer les noms d'alcool de la base aux noms de classes d'alcools extraites du site, et ainsi de les modifier.

A la fin de cette étape, nous avons une base de données de référence, qui recense les bijections trouvées entre la base ciqual et la base d'ingrédients.


## Etape 3 : Traitement des données

Dans cette partie, nous avons fait des conversions de quantités car la base ciqual nous donnait les valeurs nutritives pour 100g et que chaque cocktail avait des quantités en ml ou peu précises (ex : une tranche). En utilisant la bijection obtenue à la partie précédene entre ciqual et la liste d'ingrédients, nous avons sommé les valeurs sur tous les cocktails pour avoir à la fin l'estimation de l'apport nutritif d'un cocktails à partir des apports des différents ingrédients issus de la base Ciqual.


## Etape 4 : Identification des besoins nutritifs journaliers selon le profil de l'individu, issu de la base DRVS ?

Nous avons importé la base de données DRVs à partir du site [DRVFinder] ("https://multimedia.efsa.europa.eu/drvs/index.htm")

Ensuite : identification des nutriments intéressant, des profils à regarder (par exemple ménaupose pas intéressant), des données à récuperer sur l'individu (par exemple poids pour protéines), telles fonction

Finalement, nous retournons un graphiques (il me semble ?) des besoins journaliers selon l'individu à partir des données issu de la base DRVs.


## Etape 5 : interface pour récupérer les données de l'individu

Le but du projet était de créer une interface interactive, afin de récupérer les renseignements propre à chaque utilisateur et de proposer des cocktails "personnalisés", c'est-à-dire les plus adaptés pour l'utilisateur en question. 

Pour ce faire, nous avons utilisé le module `tkinter` . Toute cette dernière partie a été effectuée dans le fichier **interface.py** du dossier **`interface tkinter`**. Par souci de reproductibilité, cette partie ne sera pas disponible sur le notebook **nom du notebook**, mais les résultats seront présentés à l'oral.

L'interface fait apparaître quatre fenêtres.

- La première fenêtre présente la démarche à suivre à l'utilisateur.

- La deuxième fenêtre récupère les renseignements sur le profil de l'individu : on lui demande son sexe, son âge, la fréquence de son activité physique, son poids et d'autres caractéristiques liées à la maternité. Ces renseignements vont être utilisés dans le programme de l'étape 3, afin de déterminer l'apport nutritif journalier conseillé pour cette personne.

- La troisième fenêtre récupère les données sur les goûts de l'utilisateur, dans le but de lui choisir un cocktail sur mesure. La personne en question va ainsi choisir si elle veut un cocktail avec ou sans alcool, si parmi la liste d'alcools proposés il y en a qu'elle ne souhaite pas avoir et si il y a des aliments spécifiques qu'elle ne veut pas. Ces informations vont être utilisées afin d'éliminer les cocktails ne correspondant pas au désir de l'individu, et quatre cocktails seront choisi aléatoirement parmi les cocktails restant.

- La dernière fenêtre renvoie au consommateur les quatre cocktails que notre projet estime les plus proche de ses goûts, et lui montre l'apport énérgétique de chacun de ces cocktails comparé à l'apport énérgétique journalier qui lui est conseillé. Il a en particulier accès à la valeur énergétique, l'apport en eau, en protéine, en magnésium, en manganèse, en potassium et en vitamines.

## Etape 6 : Piste d'amélioration

Voici différentes suggestions d'amélioration de notre projet :
- Avoir un modèle de NLP qui nous permettrait de faire des associations de mots de manière plus précise que la reconnaissance de texte. Par exemple, ''gin'' et ''tequila'' peuvent être assimilés mais un simple algorithme de reconnaissance de texte ne peut pas les assimiler
- Compléter la base ciqual avec d'autres ingrédients et notre base de cocktails avec de nouveaux cocktails
- Coder une interface sur un autre module que tkinter, ce qui permettrait de la faire marcher sur le sspcloud et non pas uniquement en local 
