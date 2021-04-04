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