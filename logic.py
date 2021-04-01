import sqlite3
import common

def grid_to_text(grid):
	"""
	compile la grille sous forme de texte
	ligne par ligne
	un & signifie un espace
	"""
	text = ""
	for x in range(9):
		for y in range(9):
            if grid.get_number((x,y)) == 0 :
                text += "&"
            else :
			    text += str(grid.get_number((x,y)))
			
def text_to_grid(text):
    """
    Prends le texte simplifié de la grille
    et renvoie l'objet
    """
    pass

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