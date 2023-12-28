import openpyxl
import shutil
import pandas as pd

#Initialisation des variables globales
source = "/home/onyxia/work/Projet-python-2.0/main/1ou2cocktails - initial.xlsx"
#ce fichier contient les données brutes extraites du datascrapping du site 1ou2cocktails

travail = "/home/onyxia/work/Projet-python-2.0/main/travail.xlsx"
#ce fichier va etre notre fichier de travail

feuille="Maj"

ref_qte_label = "/home/onyxia/work/Projet-python-2.0/main/Cocktails - Ref - Qté.xlsx"
#dans ce fichier, les quantités des labels ont été uniformisées : par exemple, ''½ c. à thé de vanille'' est devenu	''0,5''	''c. à thé''
#cela nous permet d'avoir un format d'unité classique pour tous les ingrédients


ref_ingredient = "/home/onyxia/work/Projet-python-2.0/main/etape5.xlsx"
#pour obtenir cette table de bijection entre la table ciqual contenant les apports nutritifs et les ingrédients de nos cocktails, nous avons 

ref_unite_gr = "/home/onyxia/work/Projet-python-2.0/main/Cocktails - Ref - Unité.xlsx"
table_ciqual="/home/onyxia/work/Projet-python-2.0/main/Table Ciqual.xls"
OZ_GR = 28.3495
#[nom feuille et colonne cocktail , nom colonne mesure table ciqual]
mesure = [ 
['kcal',        'Energie, Règlement UE N° 1169/2011 (kcal/100 g)'   ] , 
['proteine',    'Protéines, N x facteur de Jones (g/100 g)'         ] , 
['glucides',    'Glucides (g/100 g)'                                ],
['calcium',     'Calcium (mg/100 g)'                                ],
 ] 

#Copie un fichier source vers un fichier cible
def copie_fichier(source,cible):
    try:
        shutil.copy2(source, cible)
        #print(f"Le fichier '{source}' a été copié avec succès vers '{cible}'.")
    except IOError as e:
        print(f"Erreur lors de la copie du fichier : {e}")

#Enregistre le fichier Excel de travail à partir d'un data frame        
def enregistre_travail(df,feuille):

    with pd.ExcelWriter(travail, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=feuille, index=False)




def sauvegarder_nouveau_fichier_excel(df, chemin_destination, nom_feuille='Feuille1'):
    """
    Sauvegarde un DataFrame dans un nouveau fichier Excel.

    :param df: DataFrame à sauvegarder.
    :param chemin_destination: Chemin complet du nouveau fichier Excel à créer.
    :param nom_feuille: Nom de la feuille de calcul dans le fichier Excel.
    """
    with pd.ExcelWriter(chemin_destination, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=nom_feuille, index=False)

# Créez un DataFrame pour tester
df_test = pd.DataFrame({'Colonne1': [1, 2, 3], 'Colonne2': ['a', 'b', 'c']})

# Utilisez la fonction pour enregistrer ce DataFrame dans un nouveau fichier Excel
chemin_destination = '/home/onyxia/work/Projet-python-2.0/main/alex.xlsx'
sauvegarder_nouveau_fichier_excel(df_test, '/home/onyxia/work/Projet-python-2.0/main/blabla.xlsx', 'MaNouvelleFeuille')



#Repete la valeur précédente d'une colonne d'un data frame
def repete_valeur_precedente(df,nom_colonne):  
    prev_value = None    
    for index, row in df.iterrows():
        # Si la cellule est vide, remplacer par la valeur précédente
        if pd.isnull(row[nom_colonne]):
            df.at[index, nom_colonne] = prev_value
        else:
            prev_value = row[nom_colonne]  

def agrege_ciqual(df_cocktail,colonne_cocktail,colonne_ciqual):
    df_ref=pd.read_excel(table_ciqual)
    #les données numériques du fichier ciqual sont au format texte
    df_cocktail['chaine'] = df_cocktail['aliment'].apply(
        lambda ref: next((champ for zone_rech, champ in zip(df_ref['alim_nom_fr'], df_ref[colonne_ciqual]) if isinstance(ref, str) and isinstance(zone_rech, str) and zone_rech in ref), None)
    )
    col1 = colonne_cocktail + '_100gr'
    #Conversion des kcal du format str au format float
    df_cocktail[col1]  = df_cocktail['chaine'].str.replace(',', '.').astype(float)
    #Suppression de la colonne chaine 
    df_cocktail = df_cocktail.drop('chaine', axis=1)
    
    
    #Nb kcal pour la quantité d'ingrédient
    col2 = 'quantity_' + colonne_cocktail
    df_cocktail[col2] =  round((df_cocktail[col1] * df_cocktail['quantity_gr'] / 100),2)

    
    feuille = 'Maj'
    #Enregistrement de la feuille dans le fichier Excel de travail
    
    enregistre_travail(df_cocktail,feuille)
        
    df1 = pd.read_excel(travail, sheet_name=feuille)
    df_cocktail = df1[['objectID', 'post_title', 'url', col2]]
    feuille = colonne_cocktail + '_cocktail'
    
    
    #Enregistrement de la feuille dans le fichier Excel de travail
    enregistre_travail(df_cocktail,feuille)

    df_cocktail = pd.read_excel(travail, sheet_name=feuille)

    col1 = 'quantity_' + colonne_cocktail + '_total'
    col2 = 'quantity_' + colonne_cocktail
    
    df_cocktail[col1] = None
    # Calcul de la somme de quantity_kcal par objectID
    df_cocktail[col1] = df_cocktail.groupby('objectID')[col2].transform('sum')
    
    df_cocktail = df_cocktail.drop(col2, axis=1)
    
    ## Suppression des lignes dupliquées pour ne conserver que la première ligne de chaque objectID
    df_cocktail = df_cocktail.drop_duplicates(subset='objectID', keep='first')
    
    #Enregistrement de la feuille dans le fichier Excel de travail
     
    enregistre_travail(df_cocktail,feuille)
    return df_cocktail















#============ DEBUT        

#Sauvegarde du fichier Excel d'init en fichier Excel de travail
copie_fichier(source,travail)

#Recopie de certaines colonnes de la feuille initiale vers une feuille Maj
df1 = pd.read_excel(travail)
df2 = df1[['objectID', 'post_title', 'url', 'ingredient', 'label', 'quantity', 'type', 'section']]

#Enregistrement de la feuille dans le fichier Excel de travail
enregistre_travail(df2,feuille)
sauvegarder_nouveau_fichier_excel(df2, '/home/onyxia/work/Projet-python-2.0/main/allez.xlsx', 'MaNouvelleFeuille')


#Suppression des lignes de la feuille Maj lorsque ingredient,label,quantity,type sont vides
df = pd.read_excel(travail, sheet_name="Maj")
df = df.dropna(subset=['ingredient', 'label','quantity','type'], how='all')

#Ajout de nouvelles colonnes vides dans la feuille Maj
liste_colonnes = ['label_zone','label_qte','label_unite','label_unite_gr',
'section_zone','section_qte','section_unite','aliment',
'kcal_100gr','quantity_gr','quantity_kcal']  

for colonne in liste_colonnes:
    df[colonne] = None

#Repete les valeurs de objectID,post_title,url sur chaque ligne
liste_colonne_a_repeter = ['objectID','post_title','url']
for colonne_a_repeter in liste_colonne_a_repeter:
    repete_valeur_precedente(df,colonne_a_repeter)

#Enregistrement de la feuille dans le fichier Excel de travail
enregistre_travail(df,feuille)
sauvegarder_nouveau_fichier_excel(df2, '/home/onyxia/work/Projet-python-2.0/main/allez2.xlsx', 'MaNouvelleFeuille')

   
df_cocktail=pd.read_excel(travail, sheet_name="Maj")
df_ref=pd.read_excel(ref_qte_label, sheet_name="Ref")

#Alimentation des colonnes label_zone,label_qte,label_unite
#Lien entre la colonne label du fichier de travail et la colonne Rech du fichier ref_qte_label
df_cocktail['label_zone'] = df_cocktail['label'].apply(
    lambda ref: next((zone_rech for zone_rech in df_ref['Rech'] if isinstance(ref, str) and isinstance(zone_rech, str) and zone_rech in ref), None)
)
df_cocktail['label_qte'] = df_cocktail['label'].apply(
    lambda ref: next((qte for zone_rech, qte in zip(df_ref['Rech'], df_ref['Qte']) if isinstance(ref, str) and isinstance(zone_rech, str) and zone_rech in ref), None)
)
df_cocktail['label_unite'] = df_cocktail['label'].apply(
    lambda ref: next((unite for zone_rech, unite in zip(df_ref['Unité'], df_ref['Unité']) if isinstance(ref, str) and isinstance(zone_rech, str) and zone_rech in ref), None)
)

#Alimentation des colonnes section_zone,section_qte,section_unite
df_cocktail['section_zone'] = df_cocktail['section'].apply(
    lambda ref: next((zone_rech for zone_rech in df_ref['Rech'] if isinstance(ref, str) and isinstance(zone_rech, str) and zone_rech in ref), None)
)
df_cocktail['section_qte'] = df_cocktail['section'].apply(
    lambda ref: next((qte for zone_rech, qte in zip(df_ref['Rech'], df_ref['Qte']) if isinstance(ref, str) and isinstance(zone_rech, str) and zone_rech in ref), None)
)
#Répéte section_qte sur chaque ligne
repete_valeur_precedente(df_cocktail,'section_qte')
df_cocktail['section_unite'] = df_cocktail['section'].apply(
    lambda ref: next((unite for zone_rech, unite in zip(df_ref['Unité'], df_ref['Unité']) if isinstance(ref, str) and isinstance(zone_rech, str) and zone_rech in ref), None)
)

#Alimentation des colonnes label_unite_gr
df_ref=pd.read_excel(ref_unite_gr)
df_cocktail['label_unite_gr'] = df_cocktail['label_unite'].apply(
    lambda ref: next((qte for zone_rech, qte in zip(df_ref['Unité'], df_ref['grammes']) if isinstance(ref, str) and isinstance(zone_rech, str) and zone_rech in ref), None)
)

#Alimentation de la colonne aliment
df_ref=pd.read_excel(ref_ingredient)
df_cocktail['aliment'] = df_cocktail['ingredient'].apply(
    lambda ref: next((champ for zone_rech, champ in zip(df_ref['Ingrédient'], df_ref['Aliment']) if isinstance(ref, str) and isinstance(zone_rech, str) and zone_rech in ref), None)
)



#Conversion de la quantité d'oz en grammes
df_cocktail['quantity_gr'] = round(df_cocktail['quantity'] * OZ_GR,2)

#Quantité en grammes issues de la colonne label
df_cocktail['label_qte_gr'] = df_cocktail['label_qte']  * df_cocktail['label_unite_gr'] 

#Alimentation de la quantité en grammes à partir de la colonne label
df_cocktail['quantity_gr'].fillna(df_cocktail['label_qte_gr'], inplace=True)

#ici
#Division de la quantité en grammes par le nombre de part(s) pour avoir une quantité par part
df_cocktail['quantity_gr'] = df_cocktail['quantity_gr'] / df_cocktail['section_qte']  

#Génère une feuille par mesure avec le total mesure par cocktail
for indice_ligne, ligne in enumerate(mesure):
    print(f"Ligne {indice_ligne}: {ligne[0]} - {ligne[1]}") 
    agrege_ciqual(df_cocktail,ligne[0],ligne[1])
    sauvegarder_nouveau_fichier_excel(agrege_ciqual(df_cocktail,ligne[0],ligne[1]), '/home/onyxia/work/Projet-python-2.0/main/' + str(ligne[0])+ '.xlsx', 'MaNouvelleFeuille')


    

