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

	Par Guilian Celin-Davanture
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
	INSERT INTO joueurs
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

def fetch_player_id(username):
	return c.execute(f"""
	SELECT id_joueur FROM joueurs WHERE pseudo = ?
	""", [username,]).fetchone()[0]

def fetch_all_grids_from_player(user_id):
	"""
	Renvoie toutes les grilles faites par un joueur

	Par Guilian Celin-Davanture
	"""
	return c.execute(f"""
	SELECT * FROM grilles WHERE id_grille in (SELECT id_grille_resolue FROM grilles_resolues WHERE id_grille_joueur = {user_id})
	""").fetchall()

def fetch_password_from_username(username):
	"""
	Renvoie le mot de passe associé au nom d'utilisateur,
	ou None si aucun utilisateur de ce nom existe.

	Par Guilian Celin-Davanture
	"""
	return c.execute(f"""
	SELECT mot_de_passe FROM joueurs WHERE pseudo = ?
	""", [username,]).fetchone()[0]

def create_relation_username_grille_id(username, grille_id):
	"""
	Va créer une relation entre un utilisateur et la grille
	désignée par l'id donnée.

	Par Guilian Celin-Davanture
	"""
	userid = c.execute(f"""
	SELECT id_joueur FROM joueurs WHERE pseudo = ?
	""", [username,]).fetchone()[0]

	# la colomne de reussite contiendra une chaine de caractères
	# correspondant à une version spécifique.
	ajouter_grilles_resolues(grille_id, userid, 'vxb1reussie')


def fetch_all_grids():
	"""
	Renvoie une liste de toutes les grilles disponibles et jouables
	(dont la difficulté est differente de 'debug', cette 'difficulté'
	marquant une grille impossible utilisée seulement pour le déboguage)

	Par Guilian Celin-Davanture
	"""
	return c.execute(f"""
	SELECT id_grille, grille, difficulte FROM grilles WHERE difficulte <> 'debug'
	""").fetchall()

def has_grid_been_done_by(grille_id, username):
	"""
	Renvoie True si la grille à été faite par le joueur.

	Par Guilian Celin-Davanture
	"""
	userid = c.execute(f"""
	SELECT id_joueur FROM joueurs WHERE pseudo = ?
	""", [username,]).fetchone()[0]

	grids = fetch_all_grids_from_player(userid)

	for grid in grids:
		id, _, _ = grid

		if id == grille_id:
			return True
			
	return False

def fetch_random_grid_with_difficulty(diff):
	"""
	Renvoie une grille aléatore avec la difficulté choisie.

	Par Guilian Celin-Davanture
	"""
	grids = c.execute(f"""
	SELECT * FROM grilles WHERE difficulte = ?
	""", [diff,]).fetchall()

	grid = random.choice(grids)

	return grid

def fetch_all_grids_with_difficulty(diff):
	"""
	Renvoie une grille aléatore avec la difficulté choisie.

	Par Guilian Celin-Davanture
	"""
	grids = c.execute(f"""
	SELECT * FROM grilles WHERE difficulte = ?
	""", [diff,]).fetchall()
	
	return grids


if __name__ == '__main__':
	curseur = c

	inp = input('Drop table ? (grilles/joueurs/grilles_resolues)')
	if inp != '':
		curseur.execute(f'DROP TABLE {inp}')
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