import tkinter as tk

fenetre = tk.Tk()
fenetre.title("Calculatrice de Furious Jumper")
fenetre.geometry("300x400")
fenetre.resizable(True, True)
fenetre.configure(bg="#2e2e2e")  # Couleur de fond sombre

# Affichage de l'écran
affichage = tk.Entry(fenetre, font=("Arial", 24), bd=10, relief=tk.RIDGE, justify="right", bg="#1e1e1e", fg="white")
affichage.grid(row=0, column=0, columnspan=4, pady=10, padx=10)

# Fonctions
def cliquer(valeur):
    affichage.insert(tk.END, valeur)

def effacer():
    affichage.delete(0, tk.END)

def calculer():
    try:
        expression = affichage.get().replace("×", "*").replace("÷", "/")
        resultat = eval(expression)
        effacer()
        affichage.insert(tk.END, str(resultat))
    except:
        effacer()
        affichage.insert(tk.END, "Erreur")

# Liste des boutons : texte, ligne, colonne
boutons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("÷", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("×", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
    ("C", 5, 0)
]

# Couleurs personnalisées
couleurs = {
    "nombres": "#3c3c3c",
    "operateurs": "#ff9500",
    "egal": "#34c759",
    "effacer": "#ff3b30",
    "texte": "white"
}

# Création des boutons
for (texte, ligne, colonne) in boutons:
    if texte == "=":
        action = calculer
        couleur = couleurs["egal"]
    elif texte == "C":
        action = effacer
        couleur = couleurs["effacer"]
    elif texte in "+-×÷":
        action = lambda val=texte: cliquer(val)
        couleur = couleurs["operateurs"]
    else:
        action = lambda val=texte: cliquer(val)
        couleur = couleurs["nombres"]

    largeur = 5 if texte != "C" else 22
    colspan = 1 if texte != "C" else 4

    bouton = tk.Button(fenetre, text=texte, width=largeur, height=2,
                       font=("Arial", 18), fg=couleurs["texte"], bg=couleur,
                       activebackground="#666666", command=action)
    bouton.grid(row=ligne, column=colonne, columnspan=colspan, padx=5, pady=5)

fenetre.mainloop()
