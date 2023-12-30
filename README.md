# **Projet Python 2A**

Erwann Hotellier • Alexia Duclert • Juliette Schneider

*Ce projet est réalisé dans le cadre du cours de Python de Lino Galiana pour l'année 2023-2024.*

Il s'agit d'un programme qui propose un choix de cocktails optimaux en terme d'apports nutritifs selon le profil et les goûts de la personne.


## Installation et utilisation

Dans le notebook **??** se trouvent les instructions détaillées pour installer les éléments requis et pour utiliser le programme.

## Etape 1 : extraction de recettes de cocktails en scrappant le site [1 ou 2 cocktails]

### Scrapping

[1 ou 2 cocktails]('https://1ou2cocktails.com/cocktails/')

Le scrapper a été codé grâce au module..., fonctionne avec ...
IL fait ... (cf exemple projet marmiton)

### Nettoyage des ingrédients

On peut alors nettoyer les ingrédients en enlevant ...
Convertir les unités en ...
on l'a fait dans le fichier **fichier.py** du dossier **dossier du fichier**.

La procédure est la suivante : (j'ai mis des idées)
- On identifie un ingrédient
- On enlève les URL
- On sépare des quantités
- On convertit...
- Comparaison avec le dico fr 


### Distance entre deux chaînes de caractères

Les ingrédients de la base sont très précis, avec un certains nombres de noms propres, en particulier pour les alcools. Dans la suite du projet, nous souhaitons sélectionner des cocktails par leurs ingrédients, afin de prendre en compte les goûts de l'utilisateur. 

Si la quantité d'ingrédient est dense est très diversifiée, le nombre d'alcool est limité. Nous avons donc décidé de simplifier tous les noms d'alcools de la base en des catégories plus grandes. Par exemple, 'gin de Palaiseau' et 'gin de New-York' deviendront 'gin', toutes les liqueurs différentes seront uniquement dénommées par 'liqueur'.

Pour ce faire, nous avons extrait du site de recette de cocktails (URL ??) les différentes classes d'alcools qu'ils considèrent. Ensuite, nous avons utilisé la **Partial Levenshtein distance (FWZ)**, implémentée par le module `fuzzywuzzy`, qui cacule la distance de Levenshtein entre la chaîne la plus courte et tous les sous-chaînes de la chaîne la plus longue de même longueur que la chaîne la plus courte, et ensuite prend le minimum de toutes ces valeurs. Cette distance nous a permis de comparer les noms d'alcool de la base aux noms de classes d'alcools extraites du site, et ainsi de les modifier.


### Sortie du scrapper

tables des recettes/ingrédients

## Etape 2 : identification des cocktails et de leurs apports nutritifs grâce à la base Ciqual

Nous avons importé la base de données Ciqual à partir du site [DataGouv] ("https://www.data.gouv.fr/fr/datasets/table-de-composition-nutritionnelle-des-aliments-ciqual/")

Ensuite (nettoyage de ciqual, sélection des colonnes qui nous intéresse, bijection des ingrédients) avec la fonction ??

Finalement, nous retournons l'estimation de l'apport nutritif d'un cocktails à partir des apports des différents ingrédients issus de la base Ciqual.

Agrégation des données :

Explication des différentes tables créées

## Etape 3 : Identification des besoins nutritifs journaliers selon le profil de l'individu, issu de la base DRVS ?

Nous avons importé la base de données DRVs à partir du site [DRV Finder]("https://multimedia.efsa.europa.eu/drvs/index.htm")

Ensuite : identification des nutriments intéressant, des profils à regarder (par exemple ménaupose pas intéressant), des données à récuperer sur l'individu (par exemple poids pour protéines), telles fonction

Finalement, nous retournons un graphiques (il me semble ?) des besoins journaliers selon l'individu à partir des données issu de la base DRVs.


## Etape 4 : interface pour récupérer les données de l'individu

Le but du projet était de créer une interface interactive, afin de récupérer les renseignements propre à chaque utilisateur et de proposer des cocktails "personnalisés", c'est-à-dire les plus adaptés pour l'utilisateur en question. 

Pour ce faire, nous avons utilisé le module `tkinter` . Toute cette dernière partie a été effectuée dans le fichier **interface.py** du dossier **`interface tkinter`**. Par souci de reproductibilité, cette partie ne sera pas disponible sur le notebook **nom du notebook**, mais les résultats seront présentés à l'oral.

L'interface fait apparaître quatre fenêtres.

- La première fenêtre présente la démarche à suivre à l'utilisateur.

- La deuxième fenêtre récupère les renseignements sur le profil de l'individu : on lui demande son sexe, son âge, la fréquence de son activité physique, son poids et d'autres caractéristiques liées à la maternité. Ces renseignements vont être utilisés dans le programme de l'étape 3, afin de déterminer l'apport nutritif journalier conseillé pour cette personne.

- La troisième fenêtre récupère les données sur les goûts de l'utilisateur, dans le but de lui choisir un cocktail sur mesure. La personne en question va ainsi choisir si elle veut un cocktail avec ou sans alcool, si parmi la liste d'alcools proposés il y en a qu'elle ne souhaite pas avoir et si il y a des aliments spécifiques qu'elle ne veut pas. Ces informations vont être utilisées afin d'éliminer les cocktails ne correspondant pas au désir de l'individu, et quatre cocktails seront choisi aléatoirement parmi les cocktails restant.

- La dernière fenêtre renvoie au consommateur les quatre cocktails que notre projet estime les plus proche de ses goûts, et lui montre l'apport énérgétique de chacun de ces cocktails comparé à l'apport énérgétique journalier qui lui est conseillé. Il a en particulier accès à la valeur énergétique, l'apport en eau, en protéine, en magnésium, en manganèse, en potassium et en vitamines.
