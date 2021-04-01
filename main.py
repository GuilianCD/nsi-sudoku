# -*- coding: utf8 -*-

"""

Ce module est le module principal.
Il contient seulement le squelette du projet
Il est le seul à contenir du code directement executable.

Les autres modules contiendront:
    Des définitions de fonctions
    Des classes
    Des asserts
    etc.
mais aucun code directement executable


Les auteurs de ce projet sont:
    * Guilian Celin-Davanture TGEN 3
    * Romain Gascoin          TGEN 9
    * Gabin Maury             TGEN 3

Version du 29/03/2021
"""


from tkinter import * 

import graphics
from theme import Themes
import common	
import random	


if __name__ == "__main__":
	root = Tk()

	root.title(common.get_random_title())

	root.resizable(False, False) #Rends la fenêtre non redimensionnable
	
	cnv=Canvas(root, width=1000, height=800, bg="ivory")
	cnv.pack(padx=0, pady=0)

	grid = common.SudokuGrid(9)

	for x in range(9):
		for y in range(9):
			grid.set_number((x, y), random.randint(0, 9))

	gridpos = (100, 100)

	#theme_bleu = Themes().BLUE

	col = ('#d1ccc0', '#FFF')

	graphics.display_grid(cnv, grid, gridpos, col)

	graphics.display_menu_around(cnv, gridpos, (0, 0), col)
	
	root.mainloop()
	