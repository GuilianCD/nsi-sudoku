"""
Module par Guilian Celin-Davanture
Permet l'affichage de la grille
"""

from tkinter import *
import random
import math
from functools import partial

import winsound

import common	
import theme



DEFAULT_SIZE = 2
	



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

	for x1 in range(grid.size):
		for y1 in range(grid.size):
			every = grid.size//3 #Tout les (taille de la grille divisée par 3 (donc 3 pour une grille normale)), changer de couleur

			ximp = (x1 // every) % 2 # (ximp : contraction de x impair) Sera 0 puis 1 tout les /every/ (every=3 <=> 0,0,0,1,1,1,0,0,etc...)
			yimp = (y1 // every) % 2 

			if ximp ^ yimp: #0 est faux, 1 est vrai
				col = theme.color_scheme['primary_light']
			else:
				col = theme.color_scheme['primary_dark']


			button = Button(tkcanvas, text=str(grid.get_number((x1, y1))), width=size*2, height=size, background=col)
			button.grid(row=(x + x1 * square_size + x1), column=(y + y1 * square_size + y1))









#class WidgetsHolder:
#	"""
#	Contiendra une liste de widgets , ce qui 
#	permettra de simplement d'iterer et de sur chaque 
#	appeler widger.grid_remove() par exemple, pour les 
#	effacer de la grille, et d'appeler la fonction show() 
#	d'un autre groupe de widgets pour l'afficher
#	"""
#
#	def __init__(self, root, width, height):
#		self.root = root
#
#		self.frame = Frame(root, width=width, height=height)
#		self.widgets = []
#
#	def add_widget(self, widget):
#		self.widgets.append(widget)
#
#	def add_widgets(self, widgets):
#		self.widgets.extend(widgets)
#
#	def hide(self):
#		for widget in self.widgets:
#			widget.grid_remove()
#
#	def show(self):
#		for widget in self.widgets:
#			widget.grid()
#





class SudokuFrame(Frame):
	def __init__(self, root, width, height, grid, grid_theme, size=2):
		super().__init__(root, width=width, height=height)


		def button_callback(x, y, button):
			#print(f"-DEBUG : Value at {x};{y} : {grid.get_number((x,y))}")
			new_text = "SUS"

			grid.set_number((x, y), new_text)
			button['text'] = new_text

			winsound.PlaySound('sound_effect.wav', winsound.SND_FILENAME)


		for x1 in range(grid.size):
			for y1 in range(grid.size):

				every = grid.size//3 #Tout les (taille de la grille divisée par 3 (donc 3 pour une grille normale)), changer de couleur

				ximp = (x1 // every) % 2 # (ximp : contraction de x impair) Sera 0 puis 1 tout les /every/ (every=3 <=> 0,0,0,1,1,1,0,0,etc...)
				yimp = (y1 // every) % 2 

				if ximp ^ yimp: #0 est faux, 1 est vrai
					col = grid_theme.color_scheme['primary_light']
				else:
					col = grid_theme.color_scheme['primary_dark']

				#Une partial est utilisée pour contrecarrer
				#le fait que referencer une variable d'une boucle
				#comme x1/y1 donnera toujours, en finalitée,
				#la derniere valeur de la boucle (ici 8/8)
				#Reference : https://stackoverflow.com/a/22290388
				button = Button(self, text=str(grid.get_number((x1, y1))), width=size*2, height=size, background=col)
				button.config(command=partial(button_callback, x1, y1, button))
				button.grid(row=x1, column=y1)



	





class Game:
	"""
	La classe SudokuGame encapsulera 
	tout le code lié au differentes pages
	de l'application (les differents menus,
	le jeu en lui-même, etc).
	04/04/2021
	"""

	def __init__(self, width, height, preset_title=""):
		self.root = Tk()
		self.root.geometry(f"{width}x{height}")
		self.root.resizable(False, False) #Rends la fenêtre non redimensionnable

		#Si preset_title n'est pas defini, il sera égal à "", ce qui est une valeur fausse
		#Donc common.get_random_title() sera appelée
		self.root.title(preset_title or common.get_random_title()) 

		self.pages = {}
		self.current_page = ""

	def mainloop(self):
		self.root.mainloop()

	def add_page(self, page, page_name):
		"""
		page_name est utilisé dans le dict pour identifer uniquement chaque
		page. Ce choix à été fait car, même si utiliser une liste semblait plus
		simple, manipuler des nombres est moins instinctif qu'utiliser des noms.
		"""
		self.pages[page_name] = page
	
	def switch_front_page_to(self, page_name):
		"""
		Affiche la page associée au nom donné après avoir masqué l'actuelle
		"""
		self.pages[self.current_page].grid_remove()
		self.pages[page_name].grid()

		self.current_page = page_name
		
