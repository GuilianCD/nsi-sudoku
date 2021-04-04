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
import theme as Themes
import common
import random	


WIDTH, HEIGHT = 1000, 800


if __name__ == "__main__":
	grid = common.SudokuGrid(9)

	for x in range(9):
		for y in range(9):
			grid.set_number((x, y), random.randint(0, 9))



	sudogame = graphics.Game(width=WIDTH, height=HEIGHT)
	
	sudoframe = graphics.SudokuFrame(sudogame.root, WIDTH, HEIGHT, grid, Themes.BLUE)
	sudoframe.pack()


	
	sudogame.mainloop()
	