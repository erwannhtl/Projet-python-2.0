from tkinter import *
import pandas as pd 
from fuzzywuzzy import fuzz
import os
import re

os.chdir('main')

## Première fenêtre expliquant les différents renseignements qui vont être demandés.

fenetre_intro = Tk()
fenetre_intro.geometry('720x720')
fenetre_intro.title("Informations générales")

#image de bar 
fond = PhotoImage(file="image-bar.png")

#mettre l'image en fond
canvas = Canvas(fenetre_intro, width=720, height=720)
canvas.place(x=0, y=0)

canvas.create_image(0, 0, anchor=NW, image=fond)

presentation = """
Afin de vous proposer les cocktails le plus adapté selon vos goûts et vos besoins nutritifs, 
nous allons vous demander par la suite des renseignements sur votre profil ainsi que vos potentielles intolérances.
Merci de cliquer sur la croix pour fermer la fenêtre afin de passer à la suite.
"""

text_widget = Text(fenetre_intro, wrap="word", height=10, width=50)
text_widget.insert(END, presentation)

#placer le texte au milieu
canvas_width = canvas.winfo_reqwidth()
canvas_height = canvas.winfo_reqheight()
text_widget_width = text_widget.winfo_reqwidth()
text_widget_height = text_widget.winfo_reqheight()

x = (canvas_width - text_widget_width) // 2
y = (canvas_height - text_widget_height) // 2

text_widget.place(x=x, y=y)

fenetre_intro.mainloop()

### Deuxième fenêtre demandant des renseignements sur le profil


fenetre_profil = Tk()
fenetre_profil.geometry('720x720')
fenetre_profil.title("Informations personnelles")

# Ajout ou suppression des boutons grossesses ...
def boutons_supplementaires():
    frame_grossesse.pack()
    frame_allaitement.pack()

def enlever_boutons():
    frame_grossesse.pack_forget()
    frame_allaitement.pack_forget()

liste = []
def ajouter_liste(event):
    lst_indice = choix_age.curselection()
    for i in lst_indice:
        age = age_possible[i]
        liste.append(age)


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
label.pack(side=TOP)

scrollbar_age = Scrollbar(frame_age, orient='vertical')

choix_age = Listbox(frame_age, selectmode = 'single',yscrollcommand=scrollbar_age.set, exportselection=0)
scrollbar_age.config(command=choix_age.yview)

age_possible = ["10 ans","11 ans","12 ans","13 ans","14 ans","15 ans","16 ans","17 ans","18-29 ans","30-39 ans","40-49 ans","50-59 ans","60-69 ans","70-79 ans","> 80 ans"]

for i in range(len(age_possible)):
    age = age_possible[i]
    choix_age.insert(i, age)

scrollbar_age.pack(side = RIGHT, fill=Y)
choix_age.pack(side = LEFT, fill = BOTH, expand = True)
choix_age.bind("<<ListboxSelect>>", ajouter_liste)

frame_age.pack(side=TOP)

# Section "Activité physique"
frame_physique = Frame(fenetre_profil)
label = Label(frame_physique, text="Fréquence de votre activité physique", font=('Helvetica', 14, 'bold'))
label.pack()
physique = StringVar()
bouton_nulle = Radiobutton(frame_physique, text="Nulle", variable=physique, value="Nulle")
bouton_faible = Radiobutton(frame_physique, text="Faible", variable=physique, value="Faible")
bouton_régulière = Radiobutton(frame_physique, text="Régulière", variable=physique, value="Régulière")
bouton_quotidienne = Radiobutton(frame_physique, text="Quotidienne", variable=physique, value="Quotidienne")

bouton_nulle.pack()
bouton_faible.pack()
bouton_régulière.pack()
bouton_quotidienne.pack()
frame_physique.pack(side = TOP)

#Section "Grossesse"
frame_grossesse = Frame(fenetre_profil)
label = Label(frame_grossesse, text="Grossesse & Allaitement", font=('Helvetica', 14, 'bold'))
label.pack(side=TOP)
label = Label(frame_grossesse, text='Si vous êtes enceinte, veuillez cochez la case correspondante', font=('Helvetica', 8))
label.pack(side=TOP)
grossesse = StringVar()
grossesse.set("None")
bouton_enceinte = Checkbutton(frame_grossesse, text="Je suis enceinte", variable=grossesse, onvalue="Je suis enceinte", offvalue='None')
bouton_enceinte.pack()

#Section "Allaitement"
frame_allaitement = Frame(fenetre_profil)
label = Label(frame_allaitement, text='Si vous allaitez, veuillez cochez la case correspondante', font=('Helvetica', 8))
label.pack(side=TOP)
allaitement = StringVar()
allaitement.set("None")
bouton_allaitement06 = Checkbutton(frame_allaitement, text="J'allaite", variable=allaitement, onvalue="J'allaite", offvalue='None')
bouton_allaitement06.pack()


fenetre_profil.mainloop()

#Récupération des données
liste = list(set(liste))
dic_profil = {"age" : liste[0], "sexe" : sexe.get(), 'activité physique': physique.get(), "spécificités" : []}
if grossesse.get() != "None":
    dic_profil["spécificités"].append(grossesse.get())
if allaitement.get() != "None":
    dic_profil["spécificités"].append(allaitement.get())


print(dic_profil)


### 3e fenêtre, pour les ingrédients des cocktails

# Charger le DataFrame depuis le fichier CSV
maj_travail = pd.read_csv('../main/maj_travail.csv', encoding='latin-1', sep = ';')

# Extraire les éléments de la colonne 'aliment' dans une liste
liste_aliments = maj_travail['aliment'].tolist()
#print(liste_aliments)
#print(len(liste_aliments))
liste_aliments_sans_doublons = list(set(liste_aliments)) #enlève les doublons
#print(liste_aliments_sans_doublons)
#print(len(liste_aliments_sans_doublons))

#séparer alcools et ingrédients - Même liste que dans le fichier cocktail.py
base_alcool = ['Gin', 'Vodka', 'Rhum','Liqueur','Tequila','Vin','Whisky','Vermouth','Crème', 'Amaretto', 'Bière', 'Cidre', 'Cognac', 'Limoncello', 'Eau-de-vie','Mezcal','Acerum','Brandy'] 

def nettoyage_alcool(l):
    #simplifier les alcools d'une liste
    n  = len(l)
    for mot in base_alcool :
        for i in range(n):
            mot_a_tester = l[i]
            ratio = fuzz.token_set_ratio(mot,mot_a_tester)
            if ratio > 95 : #si le mot de la liste l est proche de l'alcool, on le remplace par l'alcool
                l[i] = mot
    return l

liste_aliments_simplifies = nettoyage_alcool(liste_aliments_sans_doublons)
#print(liste_aliments_simplifies, len(liste_aliments_simplifies))

def suppression_alcool(l):
    #enlever les alcools d'une liste
    liste_sans_alcool = []
    for mot_a_tester in l :
        if mot_a_tester not in base_alcool:
            liste_sans_alcool.append(mot_a_tester)
    return liste_sans_alcool

liste_aliments_sans_alcools = suppression_alcool(liste_aliments_simplifies)
#print(liste_aliments_sans_alcools, len(liste_aliments_sans_alcools))

## Troisième fenêtre demandant des renseignements sur les goûts

fenetre_gout = Tk()
fenetre_gout.geometry('720x720')
fenetre_gout.title("Goûts et intolérances")
liste2 = []

def ajouter_liste2(event):
    lst_indice = choix_alcool.curselection()
    for i in lst_indice:
        alc = base_alcool[i]
        liste2.append(alc)

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

# Section Sélection Alcools
frame_nom_alcool = Frame(fenetre_gout)
label = Label(frame_nom_alcool, text="Alcools", font=('Helvetica', 14, 'bold'))
label.pack(side=TOP)
label = Label(frame_nom_alcool, text='Cochez uniquement les alcools que vous ne souhaitez pas dans votre cocktail, si il y en a', font=('Helvetica', 8))
label.pack(side=TOP)

# Ajout d'une scrollbar pour la liste de cocktails
scrollbar_alcool = Scrollbar(frame_nom_alcool, orient='vertical')

choix_alcool = Listbox(frame_nom_alcool, selectmode='multiple', yscrollcommand=scrollbar_alcool.set, exportselection=0)
scrollbar_alcool.config(command=choix_alcool.yview)

for i in range(len(base_alcool)):
    alc = base_alcool[i]
    choix_alcool.insert(i, alc)

scrollbar_alcool.pack(side = RIGHT, fill=Y)
choix_alcool.pack(side = LEFT, fill = BOTH, expand = True)
choix_alcool.bind("<<ListboxSelect>>", ajouter_liste2)

# Section Ingrédients
frame_ingredients = Frame(fenetre_gout)
label = Label(frame_ingredients, text="Ingrédients", font=('Helvetica', 14, 'bold'))
label.pack(side=TOP)
label = Label(frame_ingredients, text="Si vous avez des allergies ou ne voulez pas d'un ou plusieurs ingrédients particuliers dans votre cocktail, merci de les renseigner", font=('Helvetica', 8))
label.pack()

ingr = StringVar()
question_ingredients = Label(frame_ingredients, text = "Merci de séparer vos ingrédients d'une virgule" )
reponse_ingredient = Entry(frame_ingredients, textvariable=ingr)

question_ingredients.pack()
reponse_ingredient.pack()

frame_ingredients.pack(side=TOP)

fenetre_gout.mainloop()

#Récupération des données
liste2 = list(set(liste2))
dic_cocktails = {"Avec ou sans alcool": alcool.get(), "Alcool":[]}
if ingr.get() != '':
    dic_cocktails["Ingrédients"] = ingr.get()
dic_cocktails["Alcool"] = liste2

print(dic_cocktails)

liste_unique = []

if dic_cocktails["Avec ou sans alcool"] == "Sans alcool":
    liste_unique.extend(base_alcool)

if dic_cocktails["Alcool"]:
    liste_unique.extend(dic_cocktails["Alcool"])

if ingr.get() != '':
    liste_ingredients = re.split(r',\s*|\s*,\s*|\s*;\s*|\s+', dic_cocktails["Ingrédients"])  #sépare les ingrédients si il y en a plusieurs
    liste_unique.extend(liste_ingredients)

print(liste_unique)


#interface de cocktails à choisir
#cocktails choisi = ça 
#ressortir le graphe 










