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
	"""
	Ces trois lignes sont utilisées pour changer l'icône du programme dans la taskbar
	(absolument pas nécéssaires au reste du programme)
	https://stackoverflow.com/a/1552105
	"""
	import ctypes
	myappid = 'nsiedouardbranly.ggr.supersudoku' # ggr est l'acronyme des prénoms de chacun des membres du groupe
	ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

	grid = common.SudokuGrid(
		premade_grid=[
			[ None, None, None,  None, None, None,  None, None, None ],
			[ None, 3, None,  None, None, 9,  None, 6, None ],
			[ None, None, None,  None, None, None,  None, None, None ],
			[ 7, None, None,  None, 6, None,  None, None, None ],
			[ None, None, None,  None, None, None,  None, 8, None ],
			[ None, None, None,  None, None, 4,  None, None, None ],
			[ None, 5, None,  None, None, None,  None, None, None ],
			[ None, None, None,  None, None, None,  None, 1, None ],
			[ None, None, None,  2, None, None,  None, None, None ],
		]
	)

	"""
	for x in range(9):
		for y in range(9):
			grid.set_number((x, y), random.randint(0, 9))
	"""

	sudogame = graphics.Game(width=WIDTH, height=HEIGHT, theme=Themes.DEFAULT)
	sudogame.add_pages(graphics.get_pages(sudogame, WIDTH, HEIGHT, grid))
	sudogame.mainloop()
	