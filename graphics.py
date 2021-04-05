"""
Module par Guilian Celin-Davanture
Permet l'affichage de la grille
"""

from tkinter import *
import random
import math
from functools import partial

import common	
import theme


def get_pages(sudogame, width, height, grid, grid_theme, size=2):
	"""
	Créée toutes les pages nécéssaires à l'application.
	"""

	sudoframe = SudokuFrame(sudogame, width, height, grid, grid_theme, size=size)

	mode_menu = Frame(sudogame.root, width=width, height=height)

	mainlabel = Label(mode_menu, text="Bienvenue. Avez vous un compte ?")
	mainlabel.grid()

	guest_button = Button(mode_menu, text="Pourquoi, vous êtes flic ? (mode invité)", command=lambda : sudogame.switch_front_page_to('grid'))
	guest_button.grid()

	registered_button = Button(mode_menu, text="J'ai un compte (mode enregistré)", command=lambda : sudogame.switch_front_page_to('grid'))
	registered_button.grid()

	# ¯\_(ツ)_/¯
	exit_button = Button(mode_menu, text="J'ai ouvert ce programme par erreur", command=sudogame.root.destroy)
	exit_button.grid()


	###OPTIONS MENU
	########################################################
	gridopts = Frame(sudogame.root, width=width, height=height)

	for opt in range(9):
		y = opt // 3
		x = opt % 3

		if ((x) % 2) ^ ((y) % 2): #Expliqué plus bas (#BUTTONCOLOREXPL)
			col = grid_theme.color_scheme['primary_light']
		else:
			col = grid_theme.color_scheme['primary_dark']

		Button(gridopts, width=size*2, height=size, text=str(opt + 1), background=col, command=partial(sudoframe.update, opt)).grid(row=y, column=x)
	
	########################################################

	mode_menu.grid() # En premier car cela sera le premier menu affiché.
	sudoframe.grid()
	gridopts.grid()

	return {
		"guestmenu": mode_menu,
		"grid": sudoframe,
		"gridopts": gridopts
	}

	




class SudokuFrame(Frame):
	def __init__(self, sudogame, width, height, grid, grid_theme, size=2):
		super().__init__(sudogame.root, width=width, height=height)
		root = sudogame.root
		
		self.has_clicked = IntVar(self, value=0)

		self.mode = None

		def button_callback(pos, button):
			sudogame.switch_front_page_to("gridopts")

			self.wait_variable(self.has_clicked) #On attends un click...

			opt = self.has_clicked.get()

			grid.set_number(pos, opt)
			button['text'] = str(opt)

			#Maintenant, la valeur a été ajoutée à la grille, donc on reaffiche la grille.
			sudogame.switch_front_page_to("grid")


		#BUTTONCOLOREXPL <-------------
		#BUTTONCOLOREXPL <-------------
		#BUTTONCOLOREXPL <-------------

		every = grid.size//3 #Tout les (taille de la grille divisée par 3 (donc 3 pour une grille normale)), changer de couleur

		for x1 in range(grid.size): 
			for y1 in range(grid.size):
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
				button.config(command=partial(button_callback, (x1, y1), button))
				button.grid(row=x1, column=y1)

	def set_player_mode(self, mode):
		"""
		Mode étant soit 
		"""

	def update(self, value):
		self.has_clicked.set(value + 1)



	

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
		Il est nécéssaire d'avoir effectué page.grid(args) auparavant
		"""
		self.pages[page_name] = page

		if not self.current_page:
			self.current_page = page_name
		else:
			self.pages[page_name].grid_remove()

	def add_pages(self, pages_dict):
		for name, page in pages_dict.items():
			self.add_page(page, name)
	
	def switch_front_page_to(self, page_name):
		"""
		Affiche la page associée au nom donné après avoir masqué l'actuelle
		"""
		#print(f"Switching front page to {page_name}, in dict {self.pages}")

		
		self.pages[self.current_page].grid_remove()
		
			

		self.pages[page_name].grid()

		self.current_page = page_name

		#print(f"front page is now {self.current_page}")
		
