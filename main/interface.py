import tkinter as tk

## Première fenêtre expliquant les différents renseignements qui vont être demandés.
fenetre_intro = tk.Tk()

presentation = """
Afin de vous proposer les cocktails le plus adapté selon vos goûts et vos besoins nutritifs, nous allons vous demander par la suite des renseignements sur votre profil ainsi que vos potentielles intolérances.
Merci de cliquer sur la croix pour fermer la fenêtre afin de passer à la suite.
"""

text_widget = tk.Text(fenetre_intro, wrap="word", height=10, width=50)
text_widget.insert(tk.END, presentation)
text_widget.pack()

fenetre_intro.mainloop()


## Deuxième fenêtre demandant des renseignements sur le profil

fenetre_profil = tk.Tk()

def create_section_title(section_title):
    label = tk.Label(fenetre_profil, text=section_title, font=('Helvetica', 14, 'bold'))
    label.pack()


# Section "Sexe"
create_section_title("Sexe")
value_sexe = tk.StringVar()
bouton_homme = tk.Radiobutton(fenetre_profil, text="Homme", variable=value_sexe, value=1)
bouton_femme = tk.Radiobutton(fenetre_profil, text="Femme", variable=value_sexe, value=2)
bouton_homme.pack()
bouton_femme.pack()

# Section "Tranche d'âge"
create_section_title("Tranche d'âge")
value_age = tk.StringVar()
bouton1829 = tk.Radiobutton(fenetre_profil, text="18-29 ans", variable=value_age, value=1)
bouton_3039 = tk.Radiobutton(fenetre_profil, text="30-39 ans", variable=value_age, value=2)
bouton_4049 = tk.Radiobutton(fenetre_profil, text="40-49 ans", variable=value_age, value=3)
bouton_5059 = tk.Radiobutton(fenetre_profil, text="50-59 ans", variable=value_age, value=4)
bouton_6069 = tk.Radiobutton(fenetre_profil, text="60-69 ans", variable=value_age, value=5)
bouton_7079 = tk.Radiobutton(fenetre_profil, text="70-79 ans", variable=value_age, value=6)

bouton1829.pack()
bouton_3039.pack()
bouton_4049.pack()
bouton_5059.pack()
bouton_6069.pack()
bouton_7079.pack()

# Section "Grossesse"
create_section_title("Grossesse")
bouton_trimestre1 = tk.Checkbutton(fenetre_profil, text="Premier trimestre")
bouton_trimestre2 = tk.Checkbutton(fenetre_profil, text="Second trimestre")
bouton_trimestre3 = tk.Checkbutton(fenetre_profil, text="Troisième trimestre")

bouton_trimestre1.pack()
bouton_trimestre2.pack()
bouton_trimestre3.pack()

# Section "Allaitement"
create_section_title("Allaitement")
bouton_allaitement06 = tk.Checkbutton(fenetre_profil, text='Allaitement, 0-6 mois post partum')
bouton_allaitement6 = tk.Checkbutton(fenetre_profil, text='Allaitement, > 6 mois post partum')

bouton_allaitement06.pack()
bouton_allaitement6.pack()

# Section "Ménopause"
create_section_title("Ménopause")
bouton_postmenaupose = tk.Checkbutton(fenetre_profil, text='Post-ménopause')
bouton_premenaupose = tk.Checkbutton(fenetre_profil, text='Pré-ménopause')

bouton_postmenaupose.pack()
bouton_premenaupose.pack()


fenetre_profil.mainloop()















