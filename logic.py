import common
import random
import database
from hashlib import sha256
import copy

import solver

def grid_to_text(grid):
	"""
	compile la grille sous forme de texte
	ligne par ligne
	un & signifie un espace
	Par Romain Gascoin
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
	Par Romain Gascoin
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
	for y in range(grid_size) :
		grid_row = []
		for x in range(grid_size) :
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
			row.append(grid.get_number((x,y)))
	return rows

def squarepos(x,y):
	"""
	Fait par Gabin Maury
	Prends une position en argument et retourne le numero du carré (de 0 a 8)
	"""
	squarecoordx = str(x//3) #recupere la position x du carré actuel
	squarecoordy = str(y//3) #recupere la position y du carré actuel
	return int(squarecoordx + squarecoordy,base=3)#relie les deux positions (de 00 a 22), les considère comme un nombre en base 3 et les convertis en base 10 pour obtenir la bonne position de 0 a 8


def squares(grid):
	"""
	Fait par Gabin Maury
	Prend une grille de sudoku (objet) et retourne une liste contenant 9 listes representant les differents carrés de 3x3 dans l'ordre
	"""


	output = []
	for _ in range(grid.size):
		output.append([])
	for row, valuerow in enumerate(grid.grid):
		for column, _ in enumerate(valuerow):
			output[squarepos(row,column)].append(grid.get_number((row,column)))#on ajoute l'element actuel dans la bonne liste			
	return output

def square_to_grid(squarelist):
	"""
	Fait par Gabin Maury
	Prends la liste des carrés d'un grille et retourne la grille (objet)
	"""
	grid = []


	return grid

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


def shuffle_grid(grid):
	"""
	Fait par Gabin Maury
	prends en argument une grille de sudoku (objet) et retourne la grille
	melangée toujours valide pour creer de nouvelles grilles
	"""
	squarelist = squares(grid)
	squarerows = [squarelist[:3],squarelist[3:6],squarelist[6:]] #prends la liste des collones de carrés et la melange
	squarecolumns = [[],[],[],]
	for i in range(len(squarelist)):
		squarecolumns[i%3].append(squarelist[i])


	for i in range(random.randint()):
		pass

	newgrid = []

	return newgrid

def is_grid_full(grid):
	"""
	Renvoie vrai si la grille
	est pleine.
	Utilisée pour l'instant pour
	contrecarrer l'absence d'un
	resolveur pour analyser
	si les nombres entrés sont
	corrects

	Par Guilian Celin-Davanture
	"""
	for x in range(grid.size):
		for y in range(grid.size):
			if grid.get_number((x, y)) == None:
				return False
	return True

def get_solved_copy(grid):
	copy_grid = common.SudokuGrid(custom_grid= copy.deepcopy(grid.true_grid) )

	solver.solve_grid_v2(copy_grid)

	return copy_grid

def is_grid_solved(grid):
	"""
	Teste si la grille est résolue sans
	affecter la grille

	Par Guilian Celin-Davanture
	"""
	#On a besoin d'un vrai clonage et pas juste d'une copy 'shallow'
	copy_grid = common.SudokuGrid(custom_grid= copy.deepcopy(grid.true_grid) )

	solver.solve_grid_v2(copy_grid)

	return copy_grid.is_same_as(grid)


def hash_password(password):
	"""
	Renvoie un hash du mot de passe
	donné

	Par Guilian Celin-Davanture
	"""
	password = password.encode('utf-8')

	sha = sha256()
	sha.update( password )
	return sha.hexdigest()

def is_valid_user_pwd(username, password):
	"""
	Vérifie si le nom d'uilisateur et le
	mot de passe donnés existe dans la base
	et correspondent.

	Renvoie d'abord la réponse (True/False), puis :
		- si l'utilisateur n'existe pas dans
		la base de données, False;
		- si il existe, True.

	Par Guilian Celin-Davanture
	"""
	hashed_pwd = database.fetch_password_from_username(username)

	if hashed_pwd is None:
		return False, False

	given_pwd = hash_password(password)

	return given_pwd == hashed_pwd, True

def creer_joueur(username, rawpassword):
	"""
	Créé le joueur dans la base de données
	en hashant le mot de passe.
	"""
	password = hash_password(rawpassword)
	database.ajouter_joueur(username, password)

if __name__ == '__main__':
	from pprint import pprint
	grid = common.SudokuGrid()
	for x in range(9):
	  for y in range(9):
	    grid.set_number((x, y), random.randint(0, 9))
	pprint(rows(grid))
	pprint(columns(grid))