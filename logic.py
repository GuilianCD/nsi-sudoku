import sqlite3
import common
from math import sqrt
import random

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
	TODO retourne la liste des lignes
	"""
	return grid.grid



def columns(grid):
	"""
	TODO retourne la liste des colonnes
	"""
	columns = []
	for y in range(9):
		column = []
		for x in range(9):
			column.append(grid.get_number((x, y)))
		columns.append(column)

	return columns
		


if __name__ == '__main__':
	from pprint import pprint
	grid = common.SudokuGrid()
	for x in range(9):
	  for y in range(9):
	    grid.set_number((x, y), random.randint(0, 9))
	pprint(rows(grid))
	pprint(columns(grid))