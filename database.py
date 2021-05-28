"""
Fichier contenant tout le code relatif à
la gestion de base de données.

**************

Sauf mention contraire, tout le code
écrit dans ce fichier à été écrit par
Romain Gascoin.
"""
import random
import sqlite3

# Création de la connection à la base de données
conn = sqlite3.connect("locale/sudoku.db")

c = conn.cursor()

def commit():
	"""
	Permet de commit via une fonction
	"""
	conn.commit()

def creer_table_grilles():
	"""
	création de la table qui va contenir les différentes grilles

	Par Romain Gascoin
	"""
	c.executescript("""
	CREATE TABLE IF NOT EXISTS grilles(
	id_grille INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	grille TEXT NOT NULL UNIQUE,
	difficulte TEXT NOT NULL
	)""")
	commit()

def creer_table_joueurs():
	"""
	création de la table qui va contenir les informations à propos des joueurs

	Par Romain Gascoin
	"""
	c.executescript("""
	CREATE TABLE IF NOT EXISTS joueurs(
	id_joueur INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	pseudo TEXT NOT NULL UNIQUE,
	mot_de_passe TEXT
	)""")

	commit()

def creer_table_grilles_resolues():
	"""
	création de la table grilles résolues de relations
	grilles, joueurs qui contiendra les informations d'un joueur sur une grille donnée

	Par Romain Gascoin
	"""
	#Déplacé les déclarations FOREIGN KEY à la fin pour que cela marche (Guilian Celin-Davanture)
	c.executescript("""
	CREATE TABLE IF NOT EXISTS grilles_resolues(
	id_relation INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,

	id_grille_resolue INTEGER,
	id_grille_joueur INTEGER,
	reussite TEXT,

	FOREIGN KEY(id_grille_resolue) REFERENCES grilles(id_grille),
	FOREIGN KEY(id_grille_joueur) REFERENCES joueurs(id_joueur)
	)""")

	commit()


def ajouter_grille():
	"""
	Permet l'ajout d'une grille manuellement

	Par Romain Gascoin
	"""
	inp_grille = input("veuillez entrer une série de 81 chiffres (précédés d'un '$' si immuables (qu'on ne peut pas changer en jouant)) ou un '&' signifiant un espace")
	inp_diff = input("veuillez entrer une difficulté")

	c.execute(f"""
	INSERT INTO grilles
	(grille, difficulte)
	VALUES(?, ?)
	""", [inp_grille, inp_diff])

	commit()


def ajouter_joueur(username, password):
	c.execute(f"""
	INSERT or REPLACE INTO joueurs
	(pseudo, mot_de_passe)
	VALUES(?, ?)
	""", [username, password])
	commit()


def ajouter_grilles_resolues(id_grille, id_joueur, reussite):
	c.execute(f"""
	INSERT INTO grilles_resolues
	(id_grille_resolue, id_grille_joueur, reussite)
	VALUES(?, ?, ?)
	""", [id_grille, id_joueur, reussite])
	commit()


def fetch_all_grids_from_player(user_id):
	"""
	Renvoie toutes les grilles faites par un joueur
	"""
	return c.execute(f"""
	SELECT * FROM grilles where id_grille in (SELECT id_grille_resolue FROM grilles_resolues WHERE id_grille_joueur = {user_id})
	""").fetchall()

def fetch_all_grids():
	return c.execute(f"""
	SELECT grille, difficulte FROM grilles WHERE difficulte <> 'debug'
	""").fetchall()

def fetch_random_grid_with_difficulty(diff):
	"""
	Renvoie une grille aléatore avec la difficulté choisie.
	"""
	grids = c.execute(f"""
	SELECT grille FROM grilles WHERE difficulte = ?
	""", [diff,]).fetchall()

	grid = random.choice(grids)[0]

	return grid


if __name__ == '__main__':
	curseur = c

	inp = input('Drop ? (Y)')
	if inp == 'Y':
		curseur.execute('DROP TABLE IF EXISTS grilles')
		curseur.execute('DROP TABLE IF EXISTS joueurs')
		curseur.execute('DROP TABLE IF EXISTS grilles_resolues')
		commit()

	#Création des tables si elles n'existent pas
	creer_table_grilles()
	creer_table_joueurs()

	creer_table_grilles_resolues()

	allrows = [
				curseur.execute('SELECT * FROM grilles').fetchall(), 
				curseur.execute('SELECT * FROM joueurs').fetchall(), 
				curseur.execute('SELECT * FROM grilles_resolues').fetchall()
				]

	for rows in allrows:

		print(len(rows))
		for row in rows:
			print(row)

		print()

	try:
		while True:
			inp = input('Appuyez sur <Entrer> pour insérer, sinon eval():')
			if inp == '':
				ajouter_grille()
			else:
				eval(inp)
				commit()
	except KeyboardInterrupt:
		commit()
		curseur.close()