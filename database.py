import sqlite3

def ajouter_grilles(c):
    inp_grille = input("veuillez entrer une série de 81 chiffres (précédés d'un $) ou un & signifiant un espace (pas besoin de $)")
    inp_diff = input("difficulté ? ")

    c.execute(f"""
    INSERT INTO grilles
    (grille, difficulté)
    VALUES(?, ?)
    """, [inp_grille, inp_diff])

def ajouter_joueur(c, username, password):
    c.execute(f"""
    INSERT or REPLACE INTO joueurs
    (pseudo, mot_de_passe)
    VALUES(?, ?)
    """, [username, password])

def ajouter_grilles_resolues(c):
    c.execute(f"""
    INSERT INTO grilles_resolues
    VALUES(?, ?, ?)
    """, [id_grille_resolue, id_grille_joueur, reussite])