from tkinter import *
import pandas as pd 
from fuzzywuzzy import fuzz
import os

os.chdir('main')

## Première fenêtre expliquant les différents renseignements qui vont être demandés.
fenetre_intro = Tk()
fenetre_intro.geometry('720x720')
fenetre_intro.title("Informations générales")

presentation = """
Afin de vous proposer les cocktails le plus adapté selon vos goûts et vos besoins nutritifs, 
nous allons vous demander par la suite des renseignements sur votre profil ainsi que vos potentielles intolérances.
Merci de cliquer sur la croix pour fermer la fenêtre afin de passer à la suite.
"""

text_widget = Text(fenetre_intro, wrap="word", height=10, width=50)
text_widget.insert(END, presentation)
text_widget.pack(expand='YES')

fenetre_intro.mainloop()

### Deuxième fenêtre demandant des renseignements sur le profil

fenetre_profil = Tk()
fenetre_profil.geometry('720x720')
fenetre_profil.title("Informations personnelles")

# Ajout ou suppression des boutons grossesses ...
def boutons_supplementaires():
    frame_grossesse.pack()
    frame_allaitement.pack()
    frame_menopause.pack()

def enlever_boutons():
    frame_grossesse.pack_forget()
    frame_allaitement.pack_forget()
    frame_menopause.pack_forget()

# Section "Sexe"
frame_sexe = Frame(fenetre_profil)
label = Label(frame_sexe, text="Sexe", font=('Helvetica', 14, 'bold'))
label.pack()
sexe = StringVar()
bouton_homme = Radiobutton(frame_sexe, text="Homme", variable=sexe, value="Homme", command = enlever_boutons)
bouton_femme = Radiobutton(frame_sexe, text="Femme", variable=sexe, value="Femme", command = boutons_supplementaires)
bouton_homme.pack()
bouton_femme.pack()
frame_sexe.pack(side = TOP)

# Section "Tranche d'âge"
frame_age = Frame(fenetre_profil)
label = Label(frame_age, text="Age", font=('Helvetica', 14, 'bold'))
label.pack()
age = StringVar()
bouton1829 = Radiobutton(frame_age, text="18-29 ans", variable=age, value="18-29 ans")
bouton_3039 = Radiobutton(frame_age, text="30-39 ans", variable=age, value="30-39 ans")
bouton_4049 = Radiobutton(frame_age, text="40-49 ans", variable=age, value="40-49 ans")
bouton_5059 = Radiobutton(frame_age, text="50-59 ans", variable=age, value="50-59 ans")
bouton_6069 = Radiobutton(frame_age, text="60-69 ans", variable=age, value="60-69 ans")
bouton_7079 = Radiobutton(frame_age, text="70-79 ans", variable=age, value="70-79 ans")
bouton1829.pack()
bouton_3039.pack()
bouton_4049.pack()
bouton_5059.pack()
bouton_6069.pack()
bouton_7079.pack()
frame_age.pack(side = TOP)

#Section "Grossesse"
frame_grossesse = Frame(fenetre_profil)
label = Label(frame_grossesse, text="Grossesse", font=('Helvetica', 14, 'bold'))
label.pack()
grossesse = StringVar()
grossesse.set("None")
bouton_trimestre1 = Checkbutton(frame_grossesse, text="Premier trimestre",       variable=grossesse, onvalue="Premier trimestre", offvalue="None")
bouton_trimestre2 = Checkbutton(frame_grossesse, text="Second trimestre", variable=grossesse, onvalue="Second trimestre", offvalue="None")
bouton_trimestre3 = Checkbutton(frame_grossesse, text="Troisième trimestre", variable=grossesse, onvalue="Troisième trimestre", offvalue="None")
bouton_trimestre1.pack()
bouton_trimestre2.pack()
bouton_trimestre3.pack()


#Section "Allaitement"
frame_allaitement = Frame(fenetre_profil)
label = Label(frame_allaitement, text="Allaitement", font=('Helvetica', 14, 'bold'))
label.pack()
allaitement = StringVar()
allaitement.set("None")
bouton_allaitement06 = Checkbutton(frame_allaitement, text="Allaitement, 0-6 mois post partum", variable=allaitement, onvalue="Allaitement, 0-6 mois post partum", offvalue="None")
bouton_allaitement6 = Checkbutton(frame_allaitement, text="Allaitement, > 6 mois post partum", variable=allaitement, onvalue="Allaitement, > 6 mois post partum", offvalue="None")
bouton_allaitement06.pack()
bouton_allaitement6.pack()

#Section "Ménopause"
frame_menopause = Frame(fenetre_profil)
label = Label(frame_menopause, text="Ménopause", font=('Helvetica', 14, 'bold'))
label.pack()
menopause = StringVar()
menopause.set("None")
bouton_postmenaupose = Checkbutton(frame_menopause, text="Post-ménopause", variable=menopause, onvalue="Post-ménopause", offvalue="None")
bouton_premenaupose = Checkbutton(frame_menopause, text="Pré-ménopause", variable=menopause, onvalue="Pré-ménopause", offvalue="None")
bouton_postmenaupose.pack()
bouton_premenaupose.pack()

fenetre_profil.mainloop()

#Récupération des données
dic_profil = {"age" : age.get(), "sexe" : sexe.get()}
if grossesse.get() != "None":
    dic_profil["grossesse"] = grossesse.get()
if allaitement.get() != "None":
    dic_profil["allaitement"] = allaitement.get()
if menopause.get() != "None":
    dic_profil["menopause"] = menopause.get()

print(dic_profil)


### 3e fenêtre, pour les ingrédients des cocktails

# Charger le DataFrame depuis le fichier CSV
maj_travail = pd.read_csv('../main/maj_travail.csv', encoding='latin-1', sep = ';')

# Extraire les éléments de la colonne 'aliment' dans une liste
liste_aliments = maj_travail['aliment'].tolist()

# Afficher la liste des aliments
#print(liste_aliments)

# Enlever les doublons de la liste
liste_aliments_sans_doublons = pd.Series(liste_aliments).drop_duplicates().tolist()

# Afficher la liste des aliments sans doublons
#print(liste_aliments_sans_doublons)
#print(len(liste_aliments_sans_doublons))

#séparer alcools et ingrédients
base_alcool = ['Gin', 'Vodka', 'Rhum','Liqueur','Tequila','Vin','Whisky','Vermouth','Crème', 'Amaretto', 'Bière', 'Cidre', 'Cognac', 'Limoncello', 'Eau-de-vie','Mezcal','Acerum','Brandy'] 

## Troisième fenêtre demandant des renseignements sur les goûts

fenetre_gout = Tk()
fenetre_gout.geometry('720x720')
fenetre_gout.title("Goûts et intolérances")

def boutons_supplementaires2():
    frame_nom_alcool.pack()

def enlever_boutons2():
    frame_nom_alcool.pack_forget()

# Section "Alcools"
frame_alcool = Frame(fenetre_gout)
label = Label(frame_alcool, text="Avec ou sans alcool", font=('Helvetica', 14, 'bold'))
label.pack()
alcool = StringVar()
bouton_virgin = Radiobutton(frame_alcool, text="Sans alcool", variable=alcool, value="Sans alcool", command=enlever_boutons2)
bouton_alcool = Radiobutton(frame_alcool, text="Avec alcool", variable=alcool, value="Avec alcool", command=boutons_supplementaires2)
bouton_virgin.pack()
bouton_alcool.pack()
frame_alcool.pack(side=TOP)

# Section Ingrédients
frame_ingredients = Frame(fenetre_gout)
label = Label(frame_ingredients, text="Ingrédients", font=('Helvetica', 14, 'bold'))
label.pack(side=TOP)
label = Label(frame_ingredients, text='Cochez uniquement les ingrédients que vous ne souhaitez pas dans votre cocktail, si il y en a', font=('Helvetica', 8))
label.pack(side=TOP)
choix_ingredients = []
for mot in liste_aliments_sans_doublons:
    ingredient_var = StringVar()
    ingredient_var.set('None')
    bouton = Checkbutton(frame_ingredients, text=mot, variable=ingredient_var, onvalue=mot, offvalue='None')
    bouton.pack()
    choix_ingredients.append(ingredient_var)

frame_ingredients.pack(side=TOP)

# Section Alcools
frame_nom_alcool = Frame(fenetre_gout)
label = Label(frame_nom_alcool, text="Alcools", font=('Helvetica', 14, 'bold'))
label.pack(side=TOP)
label = Label(frame_nom_alcool, text='Cochez uniquement les alcools que vous ne souhaitez pas dans votre cocktail, si il y en a', font=('Helvetica', 8))
label.pack(side=TOP)
choix_alcool = []
for mot in base_alcool:
    nom_var = StringVar()
    nom_var.set("None")
    bouton = Checkbutton(frame_nom_alcool, text=mot, variable=nom_var, onvalue=mot, offvalue="None")
    bouton.pack()
    choix_alcool.append(nom_var)

fenetre_gout.mainloop()

#Récupération des données
dic_cocktails = {"Avec ou sans alcool": alcool.get(),"Ingrédients" :[], 'Alcool':[]}
for var in choix_ingredients : 
    if var.get() != 'None':
        dic_cocktails['Ingrédients'].append(var.get())
for alc in choix_alcool :
    if alc.get() != 'None' :
        dic_cocktails['Alcool'].append(alc.get())


print(dic_cocktails)











