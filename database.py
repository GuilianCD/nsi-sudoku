import sqlite3

def inserer_dans_grilles():
    c.execute(f"""
    INSERT INTO Grilles
    (grille, difficulté)
    VALUES({input("veuillez entrer une série de 81 chiffres (précédés d'un $) ou un & signifiant un espace (pas besoin de $)")})
    """)