"""
Module par Guilian Celin-Davanture
Permet l'affichage de la grille
"""

from tkinter import *
import random

import theme


DEFAULT_SIZE = 40




def display_rect(tkcanvas, pos, value, size=DEFAULT_SIZE, fill="#F55", width=0):
	"""
	Affiche un rectange a une certaine position selon une certaine taille.
	Ce rectangle contient une valeur (affichee)
	29/03/2021
	"""
	x, y = pos

	#width = round(width/2)

	tkcanvas.create_rectangle(x + width, 
							  y + width, 
							  x + size - width, 
							  y + size - width, 
							  fill=fill, width=width)

	tkcanvas.create_text(x + size/2, y + size/2, text=str(value))
	


def display_menu_around(tkcanvas, worldgridpos, ingridpos, colors, size=DEFAULT_SIZE):
	"""
	Affiche le menu des possibilite de valeurs sudokales (adj. relatif au sudoku)
	worldgridpos est la position de la grille dans la fenetre
	ingridpos est la position de la case visee, en coordonnes de grille (de 0 a 8 donc.)
	30/03/2021
	"""
	options = { # Les differentes positions, pour chaque nombre du menu
		1: (-1, -1),    2: ( 0, -1),    3: ( 1, -1),    
		4: (-1,  0),    5: ( 0,  0),    6: ( 1,  0),    
		7: (-1,  1),    8: ( 0,  1),    9: ( 1,  1), 
	}

	offx, offy = worldgridpos #off(set) x/y; offset de la grille
	gridx, gridy = ingridpos #Position du carre selectionne

	width = 1

	for value, pos in options.items():
		x, y = pos
		display_rect(tkcanvas, 
					 (
					 	offx + ( (gridx + x) * DEFAULT_SIZE) + (value % 3)*2*width, #offset de la grille + position du carre selectionne + pos du bouton du menu
					    offy + ( (gridy + y) * DEFAULT_SIZE) + (value // 3)*2*width
					 ),
					  value,
					  size = DEFAULT_SIZE + 6,
					  width=width
					)




def display_grid(tkcanvas, grid, pos, colors, square_size=DEFAULT_SIZE):
	"""
	Affiche une grille donnee.
	29/03/2021
	"""
	x, y = pos

	tkcanvas.create_rectangle(x-2, 
							  y-2, 
							  x + (grid.size * square_size) + grid.size + 1, 
							  y + (grid.size * square_size) + grid.size + 1, 
							  fill="#000", width=0)

	for x1 in range(grid.size):
		for y1 in range(grid.size):
			#Rouge plus fonce si pair, plus clair si impair

			ximp = (x1 // 3) % 2 # (contraction de x impair)
			yimp = (y1 // 3) % 2 # (contraction de y impair)

			col = colors[(ximp + yimp - 2 * (ximp * yimp) )] #XOR en maths 

			display_rect(tkcanvas, 
						 (x + x1 * square_size + x1,  y + y1 * square_size + y1), 
						 value=grid.get_number((x1, y1)), fill=col)

	tkcanvas.pack()
