import sqlite3
import common
from math import sqrt

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
				text += str(grid.get_number((x,y)))
	return text		

def text_to_grid(text):
	"""
	Prends le texte simplifié de la grille
	et renvoie l'objet
	"""

	text = text.split(':')
	grid_size = int(text[0]) 
	text = text[1]

	grid = []
	for x in range(grid_size):
		row = []
		for y in range(grid_size):
			val = text[x * grid_size + y]
			row.append(val if val != '&' else None)
		grid.append(row)

	sudokugrid = common.SudokuGrid(grid_size)
	sudokugrid.grid = grid #L'objet sudokugrid correspond à la grille lue

	return sudokugrid

def rows(grid):
	"""
	TODO retourne la liste des lignes
	"""
	for x in range(9):
		for y in range(9):
			pass

def collumns(grid):
	"""
	TODO retourne la liste des collones
	"""
	pass


if __name__ == '__main__':
	from pprint import pprint
	pprint(text_to_grid(grid_to_text(common.SudokuGrid())).grid)