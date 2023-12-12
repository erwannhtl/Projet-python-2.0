#Cette section permet la conversion des unités pour permettre ensuite la comparaison entre les différentes tables
#on va tout convertir en grammes

import ast
from difflib import get_close_matches
import re

# Dictionnaire de conversion
conversion = {
    'canette': 200,
    'tige': 10,
    'traits': 1,  # à remplir avec la conversion appropriée
    # Ajoute d'autres conversions au besoin
}

liste_quantites2 = '1/2 canette'

from fractions import Fraction

def convertir_fractions_en_decimal(chaine): #permet de convertir les fractions par ex 2/3 en 0.6
    fractions_trouvees = re.findall(r'\d/\d', chaine)

    for fraction_str in fractions_trouvees:
        fraction = Fraction(fraction_str)
        decimal = round(float(fraction), 1)
        chaine = chaine.replace(fraction_str, str(decimal))

    return chaine


# Fonction pour extraire la partie numérique de la chaîne
def extraire_partie_numerique(quantite):
    chiffres = re.search(r'\d+(\.\d+)?', quantite)
    if chiffres:
        return float(chiffres.group())
    return 1  # Si aucune partie numérique n'est trouvée, utilise 1 par défaut

def test(chaine):
    chaine = convertir_fractions_en_decimal(chaine)
    num=extraire_partie_numerique
#print(extraire_partie_numerique(liste_quantites2))



# Fonction pour appliquer la conversion
def convertir_en_grammes(quantite, unite):
    if isinstance(quantite, (int, float)):
        return quantite  # Si c'est déjà un nombre, pas besoin de conversion
    elif '/' in quantite:
        fraction = quantite.split('/')
        numerateur = extraire_partie_numerique(fraction[0])
        denominateur = extraire_partie_numerique(fraction[1])
        return (numerateur / denominateur) * conversion.get(unite, 1)
    else:
        quantite_numerique = extraire_partie_numerique(quantite)
        # Trouve la clé du dictionnaire la plus proche de la quantité
        clés_proches = get_close_matches(quantite, conversion.keys(), n=1, cutoff=0.6)
        if clés_proches:
            clé_proche = clés_proches[0]
            return quantite_numerique * conversion[clé_proche]
        else:
            return quantite_numerique  # Si aucune clé proche n'est trouvée, utilise la quantité numérique

# Liste initiale
#liste_quantites = [224.0, 84.0, 56.0, 112.0, 56.0, 28.0, '4 traits', '1/2 canette', '3 tiges', '3 tiges']
#liste_quantites2 = '1/2 canette'

#print(convertir_en_grammes(liste_quantites2))
# Appliquer la conversion à la liste
#liste_quantites_en_grammes = [convertir_en_grammes(quantite, unite) for quantite, unite in zip(liste_quantites2, liste_quantites2[1:])]

# Affichage du résultat
#print(liste_quantites_en_grammes)
