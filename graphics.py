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

import logic


def get_pages(sudogame, width, height, grid, size=2):
	"""
	Créée toutes les pages nécéssaires à l'application.
	"""

	grid_theme = sudogame.theme

	##################################################
	##################### Grille #####################
	##################################################

	sudoframe = SudokuFrame(sudogame, width, height, grid, size=size)

	##################################################
	################ Menu des comptes ################
	##################################################
	
	mode_menu = Frame(sudogame.root, width=width, height=height, **theme.frame(grid_theme))
	mode_menu.grid_propagate(0)

	mode_menu.grid_rowconfigure(0, weight=1)
	mode_menu.grid_columnconfigure(0, weight=1)

	mode_menu_container = Frame(mode_menu, width=width, height=height, **theme.frame(grid_theme))
	mode_menu_container.grid(row=0, column=0)

	current_row = 0
	def get_next_row():
		"""
		Permet de compter automatiquement les rows déja 
		prises et d'avoir accès à la prochaine.
		Ainsi, on a plus besoin de manuellement changer
		chaque appel à .grid(row=X)
		"""
		nonlocal current_row
		current_row += 1
		return current_row - 1

	mainlabel = Label(mode_menu_container, text="Bienvenue.", font=("Arial", 25), **theme.label(grid_theme))
	mainlabel.grid(row=get_next_row())

	#Petit espace pour séparer le "titre" du reste
	mode_menu_container.grid_rowconfigure(get_next_row(), minsize=20)

	PLACEHOLDER_COLOR = "#5c5c5c"
	TEXT_COLOR = "#000"

	def clear_placeholder(entry, placeholder, isPassword):
		if entry.get() == placeholder: #Si le texte est différent du placeholder, c'est un texte entré par l'utilisateur.
			if isPassword:
				entry.config(show='*')
			entry.config(foreground=TEXT_COLOR)
			entry.delete(0, END)

	def set_placeholder(entry, placeholder):
		if entry.get(): #Si il y a du texte, l'utilisateur a entré quelque chose
			return
		entry.config(show='')
		entry.config(foreground=PLACEHOLDER_COLOR)
		entry.insert(0, placeholder)

	#D'abord, on définit le placeholder
	USR_PLACEHOLDER = "Identifiant"
	#On définit l'entry
	usr_entry = Entry(mode_menu_container, width=60)
	#la positionne
	usr_entry.grid(row=get_next_row())
	#Quand on clique sur l'entry, si le texte est le placeholder, elle va enlever le placeholder, et remettre sa couleur de texte à noir au lieu de gris
	usr_entry.bind("<FocusIn>", lambda e : clear_placeholder(usr_entry, USR_PLACEHOLDER, False))
	#Si il n'y a rien d'écrit, Met le texte en gris, écrit le placeholder.
	usr_entry.bind("<FocusOut>", lambda e : set_placeholder(usr_entry, USR_PLACEHOLDER))
	#On appelle cette fonction pour mettre le placeholder de manière correcte.
	set_placeholder(usr_entry, USR_PLACEHOLDER)

	PWD_PLACEHOLDER = "Mot de passe"
	pwd_entry = Entry(mode_menu_container, width=60, show='*')
	pwd_entry.grid(row=get_next_row())
	#La seule différence ici est que le 3ème argument, ici True, indique que c'est un mot de passe
	#Et va donc, quand il efface le placeholder, remettre l'affichage a des étoiles (*) au lieu de texte normal
	pwd_entry.bind("<FocusIn>", lambda e : clear_placeholder(pwd_entry, PWD_PLACEHOLDER, True))
	pwd_entry.bind("<FocusOut>", lambda e : set_placeholder(pwd_entry, PWD_PLACEHOLDER))
	set_placeholder(pwd_entry, PWD_PLACEHOLDER)

	#Petit espace entre les entry fields et les boutons
	mode_menu_container.grid_rowconfigure(get_next_row(), minsize=20)


	def login(username=None, password=None):
		if (username is None) and (password is None):
			#Mode invité
			sudogame.switch_front_page_to('grid')
		else:
			if not (username and password):
				#Pas d'identifiant et/ou de mdp donné
				return
			#Mode connecté
			sudogame.switch_front_page_to('grid')


	def get_text(entry, placeholder_to_check_against):
		text = entry.get()
		if text == placeholder_to_check_against:
			return ""
		return text

	loginbutton = Button(
		mode_menu_container, 
		text='Se connecter', 
		command= ( 
			lambda : 
			login(
				get_text(usr_entry, USR_PLACEHOLDER), 
				get_text(pwd_entry, PWD_PLACEHOLDER)
			) 
		),
		**theme.button(grid_theme)
	)
	loginbutton.grid(row=get_next_row())

	#Espace en dessous pour le mode invité
	mode_menu_container.grid_rowconfigure(get_next_row(), minsize=20)

	guestlabel = Label(mode_menu_container, text="Vous souhaitez être anonyme ?", **theme.label(grid_theme))
	guestlabel.grid(row=get_next_row())

	guestlogin = Button(
		mode_menu_container, 
		text='mode invité', 
		command=login, 
		**theme.button(grid_theme))
	guestlogin.grid(row=get_next_row())

	##################################################

	mode_menu.grid() # En premier car cela sera le premier menu affiché.
	sudoframe.grid()
	#gridopts.grid()
	
	return {
		"guestmenu": mode_menu,
		"grid": sudoframe
	}



class SudokuFrame(Frame):
	def __init__(self, sudogame, width, height, grid, size=2):
		super().__init__(sudogame.root, width=width, height=height, **theme.frame(sudogame.theme))
		root = sudogame.root

		#Cette ligne permet d'ignorer le comportement de base de la Frame,
		#qui est de s'ajuster à la taille de ce qu'elle contient.
		#Ainsi, on peut redimensionner la Frame à la taille que l'on veut.
		self.grid_propagate(0) 

		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		
		#Frame contenant la Frame contenant la grille de sudoku
		#Utilisé pour centrer la grille
		gridframe = Frame(self, borderwidth=5, relief='groove')


		SETTINGS_BTN_SIZE = 10
		settings_button = Button(self, text="Options", width=SETTINGS_BTN_SIZE, height=int(SETTINGS_BTN_SIZE/2), **theme.button(sudogame.theme))
		settings_button.grid(sticky=NW)


		GRID_SIZE = width/2

		#Frame contenant la grille de sudoku
		subgridframe = Frame(gridframe, width=GRID_SIZE, height=GRID_SIZE) 
		subgridframe.grid_propagate(0) 

		subgridframe.grid(row=0, column=0)
		gridframe.grid_rowconfigure(0, weight=1)
		gridframe.grid_columnconfigure(0, weight=1)

		#Menu en dessous de la grille permettant de choisir le nombre que l'on souhaite inserer.
		#height=int(width//10) car on veut des boutons carrés et il y a 10 boutons
		gridmenu = Frame(self, width=width, height=int(width//10), borderwidth=5, relief='groove', **theme.frame(sudogame.theme))
		gridmenu.pack_propagate(0)


		self.current_option = StringVar(self, value=None)

		GRID_AND_MENU_FONT = ("Arial", 25)

		gridmenu_buttons = []
		previously_clicked_button_index = 9

		def menu_callback(text, button):
			nonlocal previously_clicked_button_index

			if text == "":
				self.current_option.set(None)
			else:
				self.current_option.set(int(text))

			gridmenu_buttons[previously_clicked_button_index]['bg'] = sudogame.theme.color_scheme['primary_light']
			gridmenu_buttons[button]['bg'] = sudogame.theme.color_scheme['primary_dark']

			previously_clicked_button_index = button

		#Les 9 chiffres + l'option de suppression
		for i in range(1, 10 + 1):
			if i == 10:
				text = ""
			else:
				text = str(i)

			button = Button(gridmenu, 
							text=text,
							background=sudogame.theme.color_scheme['primary_light'],
							command= (lambda text=text, index=i-1: menu_callback(text, index)),
							font=GRID_AND_MENU_FONT)
			button.pack(side='left', expand=True, fill='both')
			gridmenu_buttons.append(button)

		menu_callback("", previously_clicked_button_index)


		def grid_callback(pos, button):
			"""
			Appelée quand on veut remplacer un élément de la grille
			"""
			if grid.is_immutable(pos):
				pass
			else:
				opt = self.current_option.get()

				grid.set_number(pos, opt)

				if opt == str(None):
					opt = ""

				button['text'] = str(opt)

		#BUTTONCOLOREXPL <-------------
		#BUTTONCOLOREXPL <-------------

		every = grid.size//3 #Tout les (taille de la grille divisée par 3 (donc 3 pour une grille normale)), changer de couleur

		#Génération des boutons de la grille
		for x1 in range(grid.size): 
			for y1 in range(grid.size):
				ximp = (x1 // every) % 2 # (ximp : contraction de x impair) Sera 0 puis 1 tout les /every/ (every=3 <=> 0,0,0,1,1,1,0,0,etc...)
				yimp = (y1 // every) % 2 

				number = grid.get_number((x1, y1))
				if number is None:
					text = ""
				else:
					text = str(number)


				col = sudogame.theme.color_scheme['secondary_light']
				fg  = sudogame.theme.color_scheme['primary_light']

				if ximp ^ yimp: #0 est faux, 1 est vrai
					# Grâçe a ce XOR, pour chaque étape de la grille on aura :
					# 0 1 0
					# 1 0 1
					# 0 1 0
					if not grid.is_immutable((x1, y1)):
						col = sudogame.theme.color_scheme['primary_light']
						fg  = sudogame.theme.color_scheme['secondary_dark']
				else:
					if not grid.is_immutable((x1, y1)):
						col = sudogame.theme.color_scheme['primary_dark']
						fg  = sudogame.theme.color_scheme['secondary_dark']

				


				#Une partial est ici utilisée pour contrecarrer
				#le fait que referencer une variable d'une boucle
				#comme x1/y1 donnera toujours, en finalitée,
				#la derniere valeur de la boucle (ici 8/8)
				#Reference : https://stackoverflow.com/a/22290388
				button = Button(
					subgridframe, 
					text=text, 
					background=col,
					foreground=fg,
					width=int(GRID_SIZE//grid.size), 
					height=int(GRID_SIZE//grid.size),
					font=GRID_AND_MENU_FONT)

				if grid.is_immutable((x1, y1)):
					button.config(state=DISABLED)
					
				button.config(command=partial(grid_callback, (x1, y1), button))


				#     | column | column | column |
				#-----|--------|--------|--------|
				# row |		   |        |        |
				#-----|--------|--------|--------|
				# row |		   |        |        |
				#-----|--------|--------|--------|
				# row |		   |        |        |
				#-----|--------|--------|--------|
				#donc y = row et x = column
				#sticky=N+S+E+W permet au bouton de 
				#completement occuper sa case de la grille
				button.grid(row=y1, column=x1, sticky=N+S+E+W)

				subgridframe.grid_columnconfigure(x1, weight=1)
				subgridframe.grid_rowconfigure(y1, weight=1)
		

		gridframe.grid(row=0, column=0)
		gridmenu.grid(row=1, column=0)



	

class Game:
	"""
	La classe SudokuGame encapsulera 
	tout le code lié au differentes pages
	de l'application (les differents menus,
	le jeu en lui-même, etc).
	04/04/2021
	"""

	def __init__(self, width, height, theme, preset_title=""):
		self.root = Tk()
		self.root.geometry(f"{width}x{height}")
		self.root.resizable(False, False) #Rends la fenêtre non redimensionnable

		self.theme = theme

		#Si preset_title n'est pas defini, il sera égal à "", ce qui est une valeur fausse
		#Donc common.get_random_title() sera appelée
		title = preset_title or common.get_random_title()

		if title.lower() == "minecraft":
			self.root.iconbitmap("res/sudomc.ico")
		else:
			#Si aucun des cas spéciaux, l'image par défaut
			self.root.iconbitmap("res/sudoku.ico")
		
		

		self.root.title(title) 

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

		self.pages[self.current_page].grid_remove()

		self.pages[page_name].grid()

		self.current_page = page_name
		
