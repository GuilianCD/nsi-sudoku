"""
Module par Guilian Celin-Davanture
Permet l'affichage de la grille
"""

from tkinter import *
import random

import theme

import math

DEFAULT_SIZE = 2




def display_rect(tkcanvas, pos, value, size=DEFAULT_SIZE, fill="#F55", width=0):
	"""
	Affiche un rectange a une certaine position selon une certaine taille.
	Ce rectangle contient une valeur (affichee)
	29/03/2021
	"""
	x, y = pos

	#width = round(width/2)
	"""
	tkcanvas.create_rectangle(x + width, 
							  y + width, 
							  x + size - width, 
							  y + size - width, 
							  fill=fill, width=width)

	tkcanvas.create_text(x + size/2, y + size/2, text=str(value))
	"""
	


def display_values_menu(tkcanvas, worldgridpos, ingridpos, theme, size=DEFAULT_SIZE):
	"""
	Affiche le menu des possibilite de valeurs sudokales (adj. relatif au sudoku)
	worldgridpos est la position de la grille dans la fenetre
	ingridpos est la position de la case visee, en coordonnes de grille (de 0 a 8 donc.)
	30/03/2021
	"""
	offx, offy = worldgridpos #off(set) x/y; offset de la grille
	gridx, gridy = ingridpos #Position du carre selectionne

	menu_size = size * 1.1
	bubble_size = size

	for option in range(9):
		angle = (option/9) * 2 * math.pi #Angle en radians

		x = (gridx * size) + offx  +  menu_size * math.cos(angle)
		y = (gridy * size) + offy  +  menu_size * math.sin(angle) 

		tkcanvas.create_oval(
			x,
			y,
			x + bubble_size,
			y + bubble_size,
			fill="#F00"
		)




def display_grid(tkcanvas, grid, pos, theme, square_size=DEFAULT_SIZE):
	"""
	Affiche une grille donnee.
	29/03/2021
	"""
	x, y = pos

	size = DEFAULT_SIZE

	def func():
		pass

	"""
	print(int(math.sqrt(grid.size)))
	print(math.sqrt(grid.size))
	print(grid.size)
	"""

	for x1 in range(grid.size):
		for y1 in range(grid.size):
			#Rouge plus fonce si pair, plus clair si impair

			every = grid.size//3 #Tout les (taille de la grille divisée par 3 (donc 3 pour une grille normale)), changer de couleur

			ximp = (x1 // every) % 2 # (ximp : contraction de x impair) Sera 0,1,0,1, tout les /every/
			yimp = (y1 // every) % 2 

			if ximp ^ yimp: #0 est faux, 1 est vrai
				col = theme.color_scheme['primary_light']
			else:
				col = theme.color_scheme['primary_dark']


			button = Button(tkcanvas, text=str(grid.get_number((x1, y1))), width=size*2, height=size, background=col, command=func)
			button.grid(row=(x + x1 * square_size + x1), column=(y + y1 * square_size + y1))

	#tkcanvas.pack()
