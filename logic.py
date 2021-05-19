import sqlite3
import common
from math import sqrt
import random

# Création de la connection à la base de données
# Base crée dans le repertoire courant si elle n'existe pas encore
conn = sqlite3.connect("sudoku.db")

# Création d'un curseur
c = conn.cursor()

def creer_table_grilles():
	"""
	création de la table qui va contenir les différentes grilles
	"""
	c.executescript("""
	CREATE TABLE IF NOT EXISTS grilles(
	id_grille INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	grille TEXT,
	difficulte TEXT
	)""")

def creer_table_joueurs():
	"""
	création de la table qui va contenir les informations à propos des joueurs
	"""
	c.executescript("""
	CREATE TABLE IF NOT EXISTS joueurs(
	id_joueur INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	pseudo TEXT,
	)""")

def creer_relation_grilles_resolues():
	"""
	création de la relation 0N GRILLES, 0N JOUEURS qui contiendra les statistiques du joueur
	"""
	c.executescript("""
	CREATE TABLE IF NOT EXISTS grilles_resolues(
	reussite TEXT,
	temps TEXT
	)""")

def grid_to_text(grid):
	"""
	compile la grille sous forme de texte
	ligne par ligne
	un & signifie un espace
	"""
	text = f"{grid.size}:" #le premier élément du texte est la taille de la grille
	for x in range(grid.size):
		for y in range(grid.size):
			if grid.get_number((x,y)) is None:
				text += "&"
			else :
				if grid.is_immutable( (x,y) ):
					text += "$"
				text += str(grid.get_number((x,y)) )
	return text		

def text_to_grid(text):
	"""
	Prends le texte simplifié de la grille
	et renvoie l'objet
	"""

	text = text.split(':')
	grid_size = int(text[0]) 
	text = text[1]

	val_list = []
	i = 0
	while i < len(text):
		if text[i] == '&':
			val_list.append({'value': None, 'immutable': False})
		elif text[i] == '$':	#on peut regarder après car il n'y aura jamais de $ à la toute fin de text
			next_char = text[i + 1]
			val_list.append({'value': int(next_char) , 'immutable': True})
			i += 1
		else :
			val_list.append({'value': int(text[i]), 'immutable': True})
		i += 1

	grid = []
	for x in range(grid_size) :
		grid_row = []
		for y in range(grid_size) :
			grid_row.append(val_list[x * grid_size + y])
		grid.append(grid_row)

	sudokugrid = common.SudokuGrid(custom_grid = grid)


	return sudokugrid

def rows(grid):
	"""
	Fait par Gabin Maury
	Prend une grille de sudoku (objet) et retourne la liste des lignes dans l'ordre
	"""
	rows = []
	for x in range(9):
		row = []
		for y in range(9):
			row.append(grid.get_number(x,y))
	return rows


def squares(grid):
	"""
	Fait par Gabin Maury
	Prend une grille de sudoku (objet) et retourne une liste contenant 9 listes representant les differents carrés de 3x3 dans l'ordre
	"""
	def squarepos(x,y):
		"""
		Prends une position en argument et retourne le numero du carré (de 0 a 8)
		"""
		squarecoordx = str(row//3) #recupere la position x du carré actuel
		squarecoordy = str(column//3) #recupere la position y du carré actuel
		return int(squarecoordx + squarecoordy,base=3)#relie les deux positions (de 00 a 22), les considère comme un nombre en base 3 et les convertis en base 10 pour obtenir la bonne position de 0 a 8


	output = []
	for _ in range(len(grid)):
		output.append()
	for row in grid:
		for column in row:
			output[squarepos(row,column)].append(grid.get_number((row,column)))#on ajoute l'element actuel dans la bonne liste			
	return output


def columns(grid):
	"""
	Fait par Gabin Maury
	Prend une grille de sudoku (objet) et retourne la liste des colonnes dans l'ordre
	"""
	columns = []
	for y in range(9):
		column = []
		for x in range(9):
			column.append(grid.get_number((x, y)))
		columns.append(column)

	return columns

	return columns
		


if __name__ == '__main__':
	from pprint import pprint
	grid = common.SudokuGrid()
	for x in range(9):
	  for y in range(9):
	    grid.set_number((x, y), random.randint(0, 9))
	pprint(rows(grid))
	pprint(columns(grid))