import openpyxl
import shutil
import pandas as pd

#Initialisation des variables globales
source = "/home/onyxia/work/Projet-python-2.0/main/1ou2cocktails - initial.xlsx"
travail = "/home/onyxia/work/Projet-python-2.0/main/travail.xlsx"
feuille="Maj"
ref_qte_label = "/home/onyxia/work/Projet-python-2.0/main/Cocktails - Ref - Qté.xlsx"
ref_ingredient = "/home/onyxia/work/Projet-python-2.0/main/Cocktails - Ref - Ingrédients.xlsx"
ref_unite_gr = "/home/onyxia/work/Projet-python-2.0/main/Cocktails - Ref - Unité.xlsx"
table_ciqual="/home/onyxia/work/Projet-python-2.0/main/Table Ciqual.xls"
OZ_GR = 28.3495

#Copie un fichier source vers un fichier cible
def copie_fichier(source,cible):
    try:
        shutil.copy2(source, cible)
        #print(f"Le fichier '{source}' a été copié avec succès vers '{cible}'.")
    except IOError as e:
        print(f"Erreur lors de la copie du fichier : {e}")

#Enregistre le fichier Excel de travail à partir d'un data frame        
def enregistre_travail(df):
    with pd.ExcelWriter(travail, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=feuille, index=False)

#Repete la valeur précédente d'une colonne d'un data frame
def repete_valeur_precedente(df,nom_colonne):  
    prev_value = None    
    for index, row in df.iterrows():
        # Si la cellule est vide, remplacer par la valeur précédente
        if pd.isnull(row[nom_colonne]):
            df.at[index, nom_colonne] = prev_value
        else:
            prev_value = row[nom_colonne]  


            
#============ DEBUT        

#Sauvegarde du fichier Excel d'init en fichier Excel de travail
copie_fichier(source,travail)

#Recopie de certaines colonnes de la feuille initiale vers une feuille Maj
df1 = pd.read_excel(travail)
df2 = df1[['objectID', 'post_title', 'url', 'ingredient', 'label', 'quantity', 'type', 'section']]




#Enregistrement de la feuille dans le fichier Excel de travail
enregistre_travail(df2)

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
enregistre_travail(df)
   
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

#Alimentation des colonnes aliment,kcal
df_ref=pd.read_excel(ref_ingredient)
df_cocktail['aliment'] = df_cocktail['ingredient'].apply(
    lambda ref: next((champ for zone_rech, champ in zip(df_ref['Ingrédient'], df_ref['Aliment']) if isinstance(ref, str) and isinstance(zone_rech, str) and zone_rech in ref), None)
)

df_ref=pd.read_excel(table_ciqual)
#les kcal du fichier ciqual sont au format texte
df_cocktail['chaine'] = df_cocktail['aliment'].apply(
    lambda ref: next((champ for zone_rech, champ in zip(df_ref['alim_nom_fr'], df_ref['Energie, Règlement UE N° 1169/2011 (kcal/100 g)']) if isinstance(ref, str) and isinstance(zone_rech, str) and zone_rech in ref), None)
)
#Conversion des kcal du format str au format float
df_cocktail['kcal_100gr']  = df_cocktail['chaine'].str.replace(',', '.').astype(float)
#Suppression de la colonne chaine 
df_cocktail = df_cocktail.drop('chaine', axis=1)

#Conversion de la quantité d'oz en grammes
df_cocktail['quantity_gr'] = round(df_cocktail['quantity'] * OZ_GR,2)

#Quantité en grammes issues de la colonne label
df_cocktail['label_qte_gr'] = df_cocktail['label_qte']  * df_cocktail['label_unite_gr'] 

#Alimentation de la quantité en grammes à partir de la colonne label
df_cocktail['quantity_gr'].fillna(df_cocktail['label_qte_gr'], inplace=True)

#ici
#Division de la quantité en grammes par le nombre de part(s) pour avoir une quantité par part
df_cocktail['quantity_gr'] = df_cocktail['quantity_gr'] / df_cocktail['section_qte']         

#Nb kcal pour la quantité d'ingrédient
df_cocktail['quantity_kcal'] =  round((df_cocktail['kcal_100gr'] * df_cocktail['quantity_gr'] / 100),2)

#Enregistrement de la feuille dans le fichier Excel de travail
enregistre_travail(df_cocktail)

df1 = pd.read_excel(travail, sheet_name="Maj")
df_cocktail = df1[['objectID', 'post_title', 'url', 'quantity_kcal']]
feuille="Kcal_cocktail"
#Enregistrement de la feuille dans le fichier Excel de travail
enregistre_travail(df_cocktail)

df_cocktail = pd.read_excel(travail, sheet_name="Kcal_cocktail")
df_cocktail['quantity_kcal_total'] = None
# Calcul de la somme de quantity_kcal par objectID
df_cocktail['quantity_kcal_total'] = df_cocktail.groupby('objectID')['quantity_kcal'].transform('sum')

df_cocktail = df_cocktail.drop('quantity_kcal', axis=1)

## Suppression des lignes dupliquées pour ne conserver que la première ligne de chaque objectID
df_cocktail = df_cocktail.drop_duplicates(subset='objectID', keep='first')

#Enregistrement de la feuille dans le fichier Excel de travail
enregistre_travail(df_cocktail)


# Charger le fichier Excel
print(df_cocktail.head())

type_nombre = type(df_cocktail)
print(type_nombre)


# Définissez le nom et le chemin du fichier CSV
nom_fichier = 'mon_dataframe.csv'

# Ouvrez le fichier CSV
with open(nom_fichier, 'w') as f:

    # Écrivez la chaîne de caractères dans le fichier
    f.write(df_cocktail.to_string())