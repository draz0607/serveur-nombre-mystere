import tkinter as tk
from tkinter import messagebox
import random
import time
import threading
import pygame
import os

# Fichier des scores
SCORES_FILE = "scores.txt"

# Sons
VICTORY_SOUND = "win-176035.wav"
DEFEAT_SOUND = "fiasco-154915.wav"
BACKGROUND_MUSIC = "background.wav"

# Initialisation musique
pygame.mixer.init()
pygame.mixer.music.load(BACKGROUND_MUSIC)
pygame.mixer.music.play(-1)  # Boucle infinie

# Lire les scores
def lire_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    with open(SCORES_FILE, "r") as f:
        lignes = f.readlines()
    scores = []
    for ligne in lignes:
        parts = ligne.strip().split(",")
        if len(parts) == 3:
            pseudo, essais, temps = parts
            try:
                scores.append((pseudo, int(essais), float(temps)))
            except ValueError:
                continue
    return scores

# Sauvegarder un score uniquement s'il est meilleur
def sauvegarder_score(pseudo, essais, temps):
    scores = lire_scores()
    meilleur = next((s for s in scores if s[0] == pseudo), None)
    if not meilleur or (essais < meilleur[1]) or (essais == meilleur[1] and temps < meilleur[2]):
        scores = [s for s in scores if s[0] != pseudo]
        scores.append((pseudo, essais, temps))
    with open(SCORES_FILE, "w") as f:
        for s in scores:
            f.write(f"{s[0]},{s[1]},{s[2]:.2f}\n")

# Application principale
class NombreMystereApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu du Nombre Mystère")
        self.root.geometry("400x400")
        self.root.configure(bg="#1e1e2f")
        self.pseudo = ""
        self.difficulte = "Normal"
        self.essais = 0
        self.start_time = None
        self.timer_running = False
        self.valeur_max = 100
        self.creer_interface_accueil()

    def creer_interface_accueil(self):
        self.effacer_fenetre()
        tk.Label(self.root, text="Bienvenue dans le Nombre Mystère !", font=("Arial", 14), bg="#1e1e2f", fg="white").pack(pady=10)
        tk.Label(self.root, text="Entrez votre pseudo :", bg="#1e1e2f", fg="white").pack()
        self.entry_pseudo = tk.Entry(self.root)
        self.entry_pseudo.pack()

        tk.Label(self.root, text="Choisissez un niveau :", bg="#1e1e2f", fg="white").pack(pady=5)
        self.niveau_var = tk.StringVar(value="Normal")
        for niveau in ["Facile", "Normal", "Difficile"]:
            tk.Radiobutton(self.root, text=niveau, variable=self.niveau_var, value=niveau, bg="#1e1e2f", fg="white", selectcolor="#2e2e3f").pack()

        tk.Button(self.root, text="Jouer", command=self.lancer_jeu, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(self.root, text="Voir les scores", command=self.afficher_scores, bg="#2196F3", fg="white").pack(pady=5)
        tk.Button(self.root, text="Quitter", command=self.root.quit, bg="#f44336", fg="white").pack(pady=5)

    def lancer_jeu(self):
        self.pseudo = self.entry_pseudo.get().strip()
        self.difficulte = self.niveau_var.get()
        if not self.pseudo:
            messagebox.showwarning("Erreur", "Veuillez entrer un pseudo.")
            return

        if self.difficulte == "Facile":
            self.valeur_max = 50
        elif self.difficulte == "Normal":
            self.valeur_max = 100
        else:
            self.valeur_max = 200

        self.nombre_mystere = random.randint(1, self.valeur_max)
        self.essais = 0
        self.start_time = time.time()
        self.timer_running = True
        self.creer_interface_jeu()
        self.mettre_a_jour_temps()

    def creer_interface_jeu(self):
        self.effacer_fenetre()

        self.label_info = tk.Label(self.root, text=f"Trouve le nombre entre 1 et {self.valeur_max}", font=("Arial", 12), bg="#1e1e2f", fg="white")
        self.label_info.pack(pady=10)

        self.label_timer = tk.Label(self.root, text="Temps : 0 sec", bg="#1e1e2f", fg="lightgreen")
        self.label_timer.pack()

        self.label_essais = tk.Label(self.root, text="Essais : 0", bg="#1e1e2f", fg="orange")
        self.label_essais.pack()

        self.entry_nombre = tk.Entry(self.root)
        self.entry_nombre.pack(pady=10)
        self.entry_nombre.bind("<Return>", lambda event: self.verifier_nombre())

        self.label_resultat = tk.Label(self.root, text="", font=("Arial", 12), bg="#1e1e2f", fg="white")
        self.label_resultat.pack()

        self.bouton_verifier = tk.Button(self.root, text="Vérifier", command=self.verifier_nombre, bg="#00BCD4", fg="white")
        self.bouton_verifier.pack(pady=5)

        self.bouton_scores = tk.Button(self.root, text="Voir les scores", command=self.afficher_scores, bg="#2196F3", fg="white")
        self.bouton_scores.pack(pady=2)

        self.bouton_menu = tk.Button(self.root, text="Revenir au menu", command=self.creer_interface_accueil, bg="#FFC107", fg="black")
        self.bouton_menu.pack(pady=2)

        self.bouton_quitter = tk.Button(self.root, text="Quitter", command=self.root.quit, bg="#f44336", fg="white")
        self.bouton_quitter.pack(pady=2)

    def verifier_nombre(self):
        try:
            nombre = int(self.entry_nombre.get())
            self.essais += 1
            self.label_essais.config(text=f"Essais : {self.essais}")

            if nombre < self.nombre_mystere:
                self.label_resultat.config(text="Trop petit !", fg="orange")
            elif nombre > self.nombre_mystere:
                self.label_resultat.config(text="Trop grand !", fg="orange")
            else:
                self.timer_running = False
                duree = time.time() - self.start_time
                pygame.mixer.Sound(VICTORY_SOUND).play()
                self.label_resultat.config(text=f"Bravo {self.pseudo} ! Trouvé en {self.essais} essais et {int(duree)} sec.", fg="lightgreen")
                sauvegarder_score(self.pseudo, self.essais, duree)
        except ValueError:
            self.label_resultat.config(text="Veuillez entrer un nombre valide.", fg="red")

    def mettre_a_jour_temps(self):
        if self.timer_running:
            duree = int(time.time() - self.start_time)
            self.label_timer.config(text=f"Temps : {duree} sec")
            self.root.after(1000, self.mettre_a_jour_temps)

    def afficher_scores(self):
        scores = lire_scores()
        if not scores:
            messagebox.showinfo("Scores", "Aucun score enregistré.")
            return
        scores = sorted(scores, key=lambda x: (x[1], x[2]))
        message = "\n".join([f"{p} - {e} essais, {t:.1f} sec" for p, e, t in scores])
        messagebox.showinfo("Meilleurs Scores", message)

    def effacer_fenetre(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = NombreMystereApp(root)
    root.mainloop()
