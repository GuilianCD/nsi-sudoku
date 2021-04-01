import sqlite3
import common

conn = sqlite3.connect(grid)

def is_valid(grid):
	"""
	TODO
	Takes a SudokuGrid object in and returns True if it is a valid sudoku grid. Else, returns False.
	TODO
	"""
	pass


def create_full_grid():
	"""
	TODO
	Returns a solved sudoku grid created randomly
	TODO
	"""
	pass


def grid_to_text(grid):
	"""
	compile la grille sous forme de texte
	ligne par ligne
	un & signifie un espace
	"""
	text = ""
	for x in range(0,10):
		for y in range(0,10):
			text += str(grid.get_number((x,y)))
			


def rows(grid):
	"""
	TODO retourne la liste des lignes
	"""
	pass

def collumns(grid):
	"""
	TODO retourne la liste des collones
	"""
	pass