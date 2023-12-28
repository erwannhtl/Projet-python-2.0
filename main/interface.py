from tkinter import *
import pandas as pd 
from fuzzywuzzy import fuzz
import os

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
bouton_18 = Radiobutton(frame_age, text="< 18 ans", variable=age, value="< 18 ans")
bouton_1829 = Radiobutton(frame_age, text="18-29 ans", variable=age, value="18-29 ans")
bouton_3039 = Radiobutton(frame_age, text="30-39 ans", variable=age, value="30-39 ans")
bouton_4049 = Radiobutton(frame_age, text="40-49 ans", variable=age, value="40-49 ans")
bouton_5059 = Radiobutton(frame_age, text="50-59 ans", variable=age, value="50-59 ans")
bouton_6069 = Radiobutton(frame_age, text="60-69 ans", variable=age, value="60-69 ans")
bouton_7079 = Radiobutton(frame_age, text="70-79 ans", variable=age, value="70-79 ans")
bouton_80 = Radiobutton(frame_age, text="> 80 ans", variable=age, value="> 80 ans")

bouton_18.pack()
bouton_1829.pack()
bouton_3039.pack()
bouton_4049.pack()
bouton_5059.pack()
bouton_6069.pack()
bouton_7079.pack()
bouton_80.pack()
frame_age.pack(side = TOP)

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
label = Label(frame_grossesse, text="Grossesse", font=('Helvetica', 14, 'bold'))
label.pack(side=TOP)
label = Label(frame_grossesse, text='Etes-vous enceinte ou non ?', font=('Helvetica', 8))
label.pack(side=TOP)
grossesse = StringVar()
grossesse.set("None")
bouton_enceinte = Radiobutton(frame_grossesse, text="Je suis enceinte", variable=grossesse, value="Je suis enceinte")
bouton_pasenceinte = Radiobutton(frame_grossesse, text="Je ne suis pas enceinte", variable=grossesse, value="Je ne suis pas enceinte")
bouton_enceinte.pack()
bouton_pasenceinte.pack()


#Section "Allaitement"
frame_allaitement = Frame(fenetre_profil)
label = Label(frame_allaitement, text="Allaitement", font=('Helvetica', 14, 'bold'))
label.pack(side=TOP)
label = Label(frame_allaitement, text='Allaitez-vous ou non ?', font=('Helvetica', 8))
label.pack(side=TOP)
allaitement = StringVar()
allaitement.set("None")
bouton_allaitement06 = Radiobutton(frame_allaitement, text="J'allaite", variable=allaitement, value="J'allaite")
bouton_allaitement6 = Radiobutton(frame_allaitement, text="Je n'allaite pas", variable=allaitement, value="Je n'allaite pas")
bouton_allaitement06.pack()
bouton_allaitement6.pack()


fenetre_profil.mainloop()

#Récupération des données
dic_profil = {"age" : age.get(), "sexe" : sexe.get(), 'activité physique': physique.get(), "grossesse" : [], "allaitement" :[]}
if grossesse.get() != "None":
    dic_profil["grossesse"].append(grossesse.get())
if allaitement.get() != "None":
    dic_profil["allaitement"].append(allaitement.get())


print(dic_profil)


### 3e fenêtre, pour les ingrédients des cocktails

# Charger le DataFrame depuis le fichier CSV
maj_travail = pd.read_csv('../main/maj_travail.csv', encoding='latin-1', sep = ';')

# Extraire les éléments de la colonne 'aliment' dans une liste
liste_aliments = maj_travail['aliment'].tolist()
#print(liste_aliments)
#print(len(liste_aliments))
liste_aliments_sans_doublons = list(set(liste_aliments)) #enlève les doublons
print(liste_aliments_sans_doublons)
print(len(liste_aliments_sans_doublons))

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
liste1, liste2 = [], []


def ajouter_liste1(event):
    lst_indice = choix_ingredients.curselection()
    for i in lst_indice:
        ingredient = liste_aliments_sans_doublons[i]
        liste1.append(ingredient)

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
label = Label(frame_ingredients, text='Cochez uniquement les ingrédients que vous ne souhaitez pas dans votre cocktail, si il y en a', font=('Helvetica', 8))
label.pack()

# Ajout d'une scrollbar pour la liste d'ingrédients
scrollbar_ingredients = Scrollbar(frame_ingredients, orient='vertical')

choix_ingredients = Listbox(frame_ingredients, selectmode='multiple', yscrollcommand=scrollbar_ingredients.set, exportselection=0)
scrollbar_ingredients.config(command=choix_ingredients.yview)

for i in range(len(liste_aliments_sans_alcools)):
    ingredient = liste_aliments_sans_alcools[i]
    choix_ingredients.insert(i, ingredient)

scrollbar_ingredients.pack(side = RIGHT, fill=Y)
choix_ingredients.pack(side = LEFT, fill = BOTH, expand = True)
frame_ingredients.pack()
choix_ingredients.bind("<<ListboxSelect>>", ajouter_liste1)

fenetre_gout.mainloop()

#Récupération des données
liste1 = list(set(liste1))
liste2 = list(set(liste2))
dic_cocktails = {"Avec ou sans alcool": alcool.get(),"Ingrédients" :[], "Alcool":[]}
dic_cocktails['Ingrédients'] = liste1
dic_cocktails['Alcool'] = liste2

print(dic_cocktails)








