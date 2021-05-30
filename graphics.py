"""
Module par Guilian Celin-Davanture

"Permet l'affichage de la grille, entre autres."

Contient la majorité du code relatif à l'interface
graphique du sudoku, les menus, etc...
"""

from tkinter import *
import random
import math
from functools import partial

import common	
import theme

import logic
import database

from graph_utils import (
	RowCounter,
	BetterEntry
)


def get_pages(sudogame, width, height, size=2):
	"""
	Créée toutes les pages nécéssaires à l'application.
	Renvoie un dict des pages
	"""

	##################################################
	##################### Grille #####################
	##################################################

	sudoframe = SudokuFrame(sudogame, width, height, size=size)

	##################################################
	################ Menu des comptes ################
	##################################################
	
	mode_menu = create_main_menu(sudogame, width, height, size)

	##################################################
	############## Menu des difficultés ##############
	##################################################

	difficulty_menu = create_difficulty_menu(sudogame, width, height)

	##################################################
	################ Menu des grilles ################
	##################################################

	gridchoice = create_gridchoice_menu(sudogame, width, height)

	##################################################
	################ Menu des options ################
	##################################################

	optionsFrame = Frame(sudogame.root, width=width, height=height, **theme.frame(sudogame.theme))

	optionsFrame.grid_propagate(0)
	
	#Fait que le menu sera centré
	optionsFrame.grid_columnconfigure(0, weight=1)
	optionsFrame.grid_rowconfigure(0, weight=1)

	##################################################
	################ Menu des bravos #################
	##################################################

	bravoFrame = Frame(sudogame.root, width=width, height=height, **theme.frame(sudogame.theme))
	bravoFrame.grid_propagate(0)
	
	#Fait que le menu sera centré
	bravoFrame.grid_columnconfigure(0, weight=1)
	bravoFrame.grid_rowconfigure(0, weight=1)

	label = Label(bravoFrame, **theme.label(sudogame.theme), text="Bravo ! Vous avez complété la grille !", font=('Arial', 14))
	label.grid(row=1, sticky='')

	bravoFrame.grid_rowconfigure(2, minsize=10)

	back = Button(bravoFrame, text="Revenir au menu principal", width=40, height=2, **theme.button(sudogame.theme), command=lambda : sudogame.switch_front_page_to('difficultymenu'))
	back.grid(row=3)

	bravoFrame.grid_rowconfigure(4, weight=1)


	##################################################


	mode_menu.grid()
	sudoframe.grid()
	difficulty_menu.grid()
	gridchoice.grid()
	
	return {
		"guestmenu": mode_menu,
		"grid": sudoframe,
		"difficultymenu": difficulty_menu,
		"gridchoice" : gridchoice,
		"bravomenu": bravoFrame
	}, "guestmenu" #Indique quel menu sera le premier

def create_gridchoice_menu(sudogame, width, height):
	"""
	Créé le menu du choix de la grille
	"""

	"""
	Ce menu est organisé de façon compliquée.
	D'abord, on créée la frame qui contiendra la page (gridchoice_menu)
	Cette frame contiendra deux autres frames : 
		une grande en haut
		une plus petite en bas
	Celle du haut contient les grilles que l'on peut choisir,
	celle du bas contient les boutons et autres options.

	Dans la frame du haut, on insère une autre frame. On fait ceci
	pour pouvoir déplacer la dite frame via place(), pour simuler
	un effet de défilement, indisponible sur Frame.

	Dans cette derniere frame enfin, on insère une frame pour chaque
	grille de sudoku, avec les informations nécéssaires.
	"""


	gridchoice_menu = Frame(sudogame.root, width=width, height=height, **theme.frame(sudogame.theme))
	gridchoice_menu.focus()
	gridchoice_menu.grid_propagate(0)

	gridchoice_menu.grid_rowconfigure(0, weight=1)


	sudokugrids = database.fetch_all_grids()

	grids = []
	for grid in sudokugrids:
		grids.append(grid)


	BOTTOM_FRAME_SIZE = 160
	OPTION_SIZE = 140
	SPACE_BETWEEN_SIZE = 5

	content_scroll_y = IntVar(gridchoice_menu, 0)

	top_frame = Frame(gridchoice_menu, **theme.frame(sudogame.theme), width=width, height=height-BOTTOM_FRAME_SIZE)
	top_frame.grid(row=0)

	grids_content = Frame(top_frame, **theme.frame(sudogame.theme), width=width, height=(OPTION_SIZE + SPACE_BETWEEN_SIZE)*len(grids))
	grids_content.place(y=0)

	bottom_frame = Frame(
		gridchoice_menu,
		**theme.frame(sudogame.theme), 
		bg=sudogame.theme.color_scheme['secondary_dark'],
		width=width, 
		height=BOTTOM_FRAME_SIZE, 
		borderwidth=4, 
		relief=SUNKEN, 
		padx=5,
		pady=5
		)
	bottom_frame.grid_propagate(0)
	bottom_frame.grid(row=1)

	bottom_frame.grid_columnconfigure(1, weight=1)

	bottom_counter = RowCounter()

	label = Label(bottom_frame, **theme.label(sudogame.theme), text="Ou entrez votre propre grille :", font=('Arial', 14), bg=sudogame.theme.color_scheme['secondary_dark'])
	label.grid(row=bottom_counter.next(), sticky=W)

	custom_grid_entry = BetterEntry(bottom_frame, "Insérez la version texte de la grille...", width=80)
	custom_grid_entry.widget.grid(row=bottom_counter.next(), sticky=W)

	chosen_grid = IntVar(gridchoice_menu, value=-2)

	def play_grid():
		if chosen_grid.get() == -2:
			return

		if chosen_grid.get() == -1:
			grid = custom_grid_entry.get()
		else:
			grid = grids[chosen_grid.get()][1]

		sudogame.grid.set(grid) 
		sudogame.get_page("grid").init_grid()

		sudogame.switch_front_page_to("grid")

	Button(bottom_frame, text="Selectionner cette grille", **theme.button(sudogame.theme), command=lambda : chosen_grid.set(-1)).grid(row=bottom_counter.next(), sticky=W)

	bottom_frame.grid_rowconfigure(bottom_counter.next(), weight=1)

	Button(bottom_frame, text="Jouer !", width=16, height=4, **theme.button(sudogame.theme), command=play_grid).grid(row=bottom_counter.next(), column=2, sticky=SE)


	content_counter = RowCounter()

	for index, grid in enumerate(grids):
		_, grille, difficulte = grid

		i = content_counter.next()
		fr = Frame(grids_content, **theme.frame(sudogame.theme), height=OPTION_SIZE, width=width, borderwidth=4, relief=RIDGE)
		fr.grid_propagate(0)
		fr.grid(row=i)

		curr_grid = logic.text_to_grid(grille)

		CNV_BOX_SIZE = 13
		HALF_BOX = 7
		CNV_OFFSET = 2

		cnv_width = CNV_BOX_SIZE * curr_grid.size
		cnv_height= CNV_BOX_SIZE * curr_grid.size

		cnv = Canvas(fr, width=cnv_width - 2 *CNV_OFFSET, height=cnv_height - 2 * CNV_OFFSET, borderwidth=0, highlightthickness=0)

		cnv.create_rectangle(0, 0, cnv_width, cnv_height, fill='black')

		for x in range(curr_grid.size + 1):
			for y in range(curr_grid.size + 1):
				x1, y1 = CNV_OFFSET + x + x * CNV_BOX_SIZE, CNV_OFFSET + y + y * CNV_BOX_SIZE

				cnv.create_rectangle(x1, y1, x1 + CNV_BOX_SIZE, y1 + CNV_BOX_SIZE , fill='white')

				cnv.create_text(x1 - HALF_BOX, y1 - HALF_BOX, text=curr_grid.get_number((x-1, y-1)))

		cnv.grid(row=0, rowspan=10)


		Label(fr, text="Grille #" + str(index+1), **theme.label(sudogame.theme), font=('Arial', 30)).grid(row=1, column=1, sticky=W)
		
		Label(fr, text="Difficulté : " + str(difficulte), **theme.label(sudogame.theme), font=('Arial', 10)).grid(row=2, column=1, sticky=W)

		fr.grid_rowconfigure(3, weight=1)
		fr.grid_columnconfigure(2, weight=1)

		Button(fr, text="Selectionner", **theme.button(sudogame.theme), command=lambda : chosen_grid.set(index)).grid(row=4, column=2, sticky=SE)


		grids_content.grid_rowconfigure(content_counter.next(), minsize=SPACE_BETWEEN_SIZE)

	SCROLL_DELTA = 25
	
	def scroll_content(event):
		"""
		Va tenter de faire défiler le menu.
		Si la taille du menu défilable est plus petite que celle
		du contenant, on ne défile pas.
		Sinon, on ajoute SCROLL_DELTA * (event.delta / abs(event.delta)) 
		a l'offset. Ce nombre est une constante multiplié soit par 1 si 
		le delta est positif (si x>0, x/abs(x) = 1) ou -1 si négatif
		(si x<0, x/abs(x) = -1).
		Si le menu défilable dépasse, on le remet aux bonnes coordonnées.
		Ainsi, le contenant est toujours plein du menu défilable.
		"""
		if grids_content.winfo_height() <= (height - BOTTOM_FRAME_SIZE):
			return

		new_offset = content_scroll_y.get() + SCROLL_DELTA * (event.delta / abs(event.delta))
		if new_offset > 0:
			new_offset = 0

		if new_offset - (height - BOTTOM_FRAME_SIZE) < -1 * grids_content.winfo_height():
			new_offset = -1 * grids_content.winfo_height() + (height - BOTTOM_FRAME_SIZE)
		
		

		content_scroll_y.set(new_offset)

		grids_content.place_configure(x=0, y=content_scroll_y.get())

	sudogame.root.bind("<MouseWheel>", scroll_content)

	return gridchoice_menu


def create_difficulty_menu(sudogame, width, height):
	"""
	Créé le menu du choix de la difficulté
	"""
	current_theme = sudogame.theme

	difficulty_menu = Frame(sudogame.root, width=width, height=height, **theme.frame(current_theme))
	difficulty_menu.grid_propagate(0)

	counter = RowCounter()

	def difficulty_callback(difficulty, play_new):
		if difficulty != '':
			"""
			#Debug
			sudogame.grid.set("9:&&&&&&&&&&$3&&&$9&$6&&&&&&&&&&$7&&&$6&&&&&&&&&&&$8&&&&&&$4&&&&$5&&&&&&&&&&&&&&$1&&&&$2&&&&&")
			"""
			id, grille, _ = database.fetch_random_grid_with_difficulty(difficulty)

			#Variable qui sera 1 si il à été impossible de trouver une grille
			#jamais faite par le joueur.
			unable_to_new = IntVar(difficulty_menu, 0)

			if play_new:
				"""
				while database.has_grid_been_done_by(id, ):
					id, grille, _ = database.fetch_random_grid_with_difficulty(difficulty)
				"""

				played_grids = database.fetch_all_grids_from_player(database.fetch_player_id(sudogame.identifiers[0]))

				#Trie toutes les grilles du joueur et ne garde que celle dont la difficulté est de celle recherchée.
				played_grids_with_difficulty = []
				for grid in played_grids:
					_, _, grid_diff = grid
					if grid_diff == difficulty:
						played_grids_with_difficulty.append(grid)
					

				all_grids = database.fetch_all_grids_with_difficulty(difficulty)

				if len(all_grids) <= len(played_grids_with_difficulty):
					#Impossible de jouer une grille jamais jouée ; le joueur à joué toutes les grilles de cette difficulté.
					unable_to_new.set(1)
					pass
				else:
					while True:
						grid = database.fetch_random_grid_with_difficulty(difficulty)
						if grid not in played_grids_with_difficulty:
							id, grille, _ = grid
							break


			sudogame.grid.set(grille)
			sudogame.get_page("grid").init_grid()

			sudogame.grid_db_id = id

			if unable_to_new.get() == 1:
				already_played.set('Vous avez joué toutes les grilles disponibles ! Chargement d\'une grille déja jouée...')
				difficulty_menu.after(4000, lambda : sudogame.switch_front_page_to("grid") )
			else:
				sudogame.switch_front_page_to("grid")
		else:
			sudogame.difficulty.set(difficulty)		
			sudogame.switch_front_page_to("gridchoice")		

	#Fait que la colonne prendra le maximum d'espace disponible
	difficulty_menu.grid_columnconfigure(0, weight=1)

	# Ici, on créé les boutons du menu de choix
	# de difficulté. On sépare chacun de ces boutons
	# part un espace, qui est créé grâçe à un 
	# "difficulty_menu.grid_rowconfigure(counter.next(), weight=XX)"
	# qui est intercalé entre chaque bouton ou label

	difficulty_menu.grid_rowconfigure(counter.next(), weight=100)

	label = Label(difficulty_menu, text="Choissisez une difficulté.", **theme.label(current_theme), font=("Arial", 25))
	label.grid(row=counter.next())    

	difficulty_menu.grid_rowconfigure(counter.next(), weight=10)

	play_new = IntVar(difficulty_menu, 0)

	Checkbutton(difficulty_menu, text="Jouer uniquement de nouvelles grilles",variable=play_new, onvalue=1, offvalue=0).grid(row=counter.next()) 

	difficulty_menu.grid_rowconfigure(counter.next(), weight=3)

	already_played = StringVar(difficulty_menu, '')

	already_played_label = Label(difficulty_menu, textvariable=already_played, **theme.label(current_theme), font=("Arial", 10), fg='red')
	already_played_label.grid(row=counter.next())  

	difficulty_menu.grid_rowconfigure(counter.next(), weight=3) 

	BTN_WIDTH = 10
	
	easy_btn   = Button(difficulty_menu, text="Facile",  command=lambda : difficulty_callback("facile", play_new),   **theme.button(current_theme), width=BTN_WIDTH)
	easy_btn.grid(row=counter.next())

	difficulty_menu.grid_rowconfigure(counter.next(), weight=1)

	medium_btn = Button(difficulty_menu, text="Moyen",   command=lambda : difficulty_callback("moyenne", play_new), **theme.button(current_theme), width=BTN_WIDTH)
	medium_btn.grid(row=counter.next())

	difficulty_menu.grid_rowconfigure(counter.next(), weight=1)

	expert_btn = Button(difficulty_menu, text="Expert",  command=lambda : difficulty_callback("difficile", play_new), **theme.button(current_theme), width=BTN_WIDTH)
	expert_btn.grid(row=counter.next())

	difficulty_menu.grid_rowconfigure(counter.next(), weight=10)

	expert_btn = Button(difficulty_menu, text="Lister toutes les grilles",  command=lambda : difficulty_callback("", play_new), **theme.button(current_theme), width=BTN_WIDTH * 2)
	expert_btn.grid(row=counter.next())

	difficulty_menu.grid_rowconfigure(counter.next(), weight=100)

	return difficulty_menu


def create_main_menu(sudogame, width, height, size):
	"""
	Créé le menu de choix du mode (invité ou utilisateur)
	"""
	grid_theme = sudogame.theme

	mode_menu = Frame(sudogame.root, width=width, height=height, **theme.frame(grid_theme))
	mode_menu.grid_propagate(0)

	mode_menu.grid_rowconfigure(0, weight=1)
	mode_menu.grid_columnconfigure(0, weight=1)

	mode_menu_container = Frame(mode_menu, width=width, height=height, **theme.frame(grid_theme))
	mode_menu_container.grid(row=0, column=0)

	counter = RowCounter()

	mainlabel = Label(mode_menu_container, text="Bienvenue.", font=("Arial", 25), **theme.label(grid_theme))
	mainlabel.grid(row=counter.next())

	sublabel = Label(mode_menu_container, text="Un compte sera créé si vous essayez de vous connecter à un compte inexistant.", font=("Arial", 10), **theme.label(grid_theme))
	sublabel.grid(row=counter.next())

	#Petit espace pour séparer le "titre" du reste
	mode_menu_container.grid_rowconfigure(counter.next(), minsize=10)

	login_result_text = StringVar(mode_menu_container, '')
	login_result_label = Label(mode_menu_container, textvariable=login_result_text, font=("Arial", 16), **theme.label(grid_theme), fg='red')
	login_result_label.grid(row=counter.next())

	mode_menu_container.grid_rowconfigure(counter.next(), minsize=10)

	USR_PLACEHOLDER = "Identifiant"
	PWD_PLACEHOLDER = "Mot de passe"

	usr_entry = BetterEntry(mode_menu_container, USR_PLACEHOLDER, width=60)
	usr_entry.widget.grid(row=counter.next())

	pwd_entry = BetterEntry(mode_menu_container, PWD_PLACEHOLDER, is_password=True, width=60)
	pwd_entry.widget.grid(row=counter.next())

	#Petit espace entre les entry fields et les boutons
	mode_menu_container.grid_rowconfigure(counter.next(), minsize=20)


	def login(username=None, password=None):
		if (username is None) and (password is None):
			#Mode invité
			sudogame.switch_front_page_to('difficultymenu')
		else:
			if not (username and password):
				#Pas d'identifiant et/ou de mdp donné
				login_result_text.set("Veuillez remplir les cases pour vous connecter.")
				return
			#Mode connecté

			valid, exists_in_db = logic.is_valid_user_pwd(username, password)

			if not exists_in_db:
				logic.creer_joueur(username, password)
			else:
				if not valid:
					login_result_text.set("Veuillez entrer le mot de passe correspondant au nom d'uilisateur")
					return

			#Sera utile plus tard
			sudogame.identifiers = (username, password)

			sudogame.switch_front_page_to('difficultymenu')



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
	loginbutton.grid(row=counter.next())

	#Espace en dessous pour le mode invité
	mode_menu_container.grid_rowconfigure(counter.next(), minsize=20)

	guestlabel = Label(mode_menu_container, text="Vous souhaitez être anonyme ?", **theme.label(grid_theme))
	guestlabel.grid(row=counter.next())

	guestlogin = Button(
		mode_menu_container, 
		text='mode invité', 
		command=login, 
		**theme.button(grid_theme))
	guestlogin.grid(row=counter.next())

	return mode_menu


class SudokuFrame(Frame):
	def __init__(self, sudogame, width, height, size=2):
		super().__init__(sudogame.root, width=width, height=height, **theme.frame(sudogame.theme))
		root = sudogame.root

		#On garde une référence
		self.sudogame = sudogame

		#Gardera une trace des coups joués
		self.history = []

		#Cette ligne permet d'ignorer le comportement de base de la Frame,
		#qui est de s'ajuster à la taille de ce qu'elle contient.
		#Ainsi, on peut redimensionner la Frame à la taille que l'on veut.
		self.grid_propagate(0) 

		self.grid_rowconfigure(0, weight=1)
		
		#Frame contenant la Frame contenant la grille de sudoku
		#Utilisé pour centrer la grille
		gridframe = Frame(self, borderwidth=5, relief='groove')

		
		SETTINGS_BTN_SIZE = 10
		settings_button = Button(self, text="Options", width=SETTINGS_BTN_SIZE, height=int(SETTINGS_BTN_SIZE/2), **theme.button(sudogame.theme))
		settings_button.grid(row=0, column=0, sticky=NW)
		
		

		UNDO_BTN_SIZE = 6
		undo_button = Button(
			self, 
			text="Ctrl+Z", 
			width=UNDO_BTN_SIZE, 
			height=int(UNDO_BTN_SIZE/2), 
			**theme.button(sudogame.theme), 
			command=self.undo)
		undo_button.grid(row=0, column=2, sticky=SE)

		self.undo_btn = undo_button

		self.turn_off_undo()


		GRID_SIZE = width/2
		self.GRID_SIZE = GRID_SIZE

		#Frame contenant la grille de sudoku
		subgridframe = Frame(gridframe, width=GRID_SIZE, height=GRID_SIZE) 
		subgridframe.grid_propagate(0) 

		#Cette référence est utilisée pour créer dynamiquement la grille de sudoku
		self.subgridframe = subgridframe

		subgridframe.grid(row=0, column=0)
		gridframe.grid_rowconfigure(0, weight=1)
		gridframe.grid_columnconfigure(0, weight=1)

		#Menu en dessous de la grille permettant de choisir le nombre que l'on souhaite inserer.
		#height=int(width//10) car on veut des boutons carrés et il y a 10 boutons
		gridmenu = Frame(self, width=width, height=int(width//10), borderwidth=5, relief='groove', **theme.frame(sudogame.theme))
		gridmenu.pack_propagate(0)


		self.current_option = StringVar(self, value=None)

		GRID_AND_MENU_FONT = ("Arial", 25)
		self.GRID_AND_MENU_FONT = GRID_AND_MENU_FONT

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



		#Garde une référence de tout les boutons de la grille
		self.gridbuttons = []

		gridframe.grid(row=0, column=1, sticky="")
		gridmenu.grid(row=1, column=0, columnspan=3)

	def init_grid(self):
		subgridframe = self.subgridframe
		sudogame = self.sudogame
		GRID_SIZE = self.GRID_SIZE
		GRID_AND_MENU_FONT = self.GRID_AND_MENU_FONT

		grid = logic.text_to_grid(sudogame.grid.get())
		self.sudogrid = grid

		def grid_callback(pos, button):
			"""
			Appelée quand on veut remplacer un élément de la grille
			"""
			if grid.is_immutable(pos):
				pass
			else:
				opt = self.current_option.get()
	
				if grid.get_number(pos) == opt:
					return
				if (grid.get_number(pos) is None) and (opt == str(None)):
					return
				
				self.play(pos, opt, grid.get_number(pos))

				grid.set_number(pos, opt)

				if opt == str(None):
					opt = ""

				button['text'] = str(opt)
				
				#FIXME La deuxième condition (True) est ici pour rappeler qu'il faut
				#	   implémenter les tests relatifs au solveur.
				if logic.is_grid_full(grid) and True:
					#Ici on considère que l'utilisateur à terminé sa partie.
					#On enregistre donc ceci dans la base de données.

					database.create_relation_username_grille_id(sudogame.identifiers[0], sudogame.grid_db_id)

					sudogame.switch_front_page_to('bravomenu')


		#BUTTONCOLOREXPL <-------------
		#BUTTONCOLOREXPL <-------------

		every = grid.size//3 #Tout les (taille de la grille divisée par 3 (donc 3 pour une grille normale)), changer de couleur

		#Génération des boutons de la grille
		for x1 in range(grid.size): 
			#print(f'-> x looping... ({x1})')
			gridbuttonarray = []
			for y1 in range(grid.size):
				#print(f'-> -> y looping... ({y1})')
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

				gridbuttonarray.append(button)

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
		
			self.gridbuttons.append(gridbuttonarray)


	def turn_off_undo(self):
		self.undo_btn.config(state=DISABLED, bg=self.sudogame.theme.color_scheme['button_disabled'])

	def turn_on_undo(self):
		self.undo_btn.config(state=NORMAL, bg=self.sudogame.theme.color_scheme['button_normal'])

	def play(self, pos, value, previous_value):
		self.history.append({'pos': pos, 'value': value, 'previous': previous_value})

		self.turn_on_undo()

	def undo(self):
		grid = self.sudogrid

		if index_plus_1 := len(self.history): #Seulement si l'historique des coups contient >= 1 élément.
			latest_play = self.history.pop(index_plus_1 - 1)

			pos, value = latest_play['pos'], latest_play['previous']

			grid.set_number(pos=pos, value=value) 

			self.gridbuttons[pos[0]]
			self.gridbuttons[pos[0]][pos[1]]

			self.gridbuttons[pos[0]][pos[1]]['text'] = str(value) if not (value in [None, 'None']) else ""

			if len(self.history) == 0:
				self.turn_off_undo()

			return latest_play
		

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
		
		self.difficulty = StringVar(self.root, value="")

		self.root.title(title) 

		self.pages = {}
		self.current_page = ""

		#Cet attribut stockera les identifiants de l'utilisateur actuel
		self.identifiers = (None, None)

		#Cet attribut stockera la clé primaire de la grille dans la base de données.
		self.grid_db_id = -1

		self.grid = StringVar(self.root)

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

	def get_page(self, page_name):
		return self.pages[page_name]

	def add_pages(self, pages_dict, first_page_name):
		self.add_page(pages_dict[first_page_name], first_page_name)

		for name, page in pages_dict.items():
			if name == first_page_name:
				continue
			self.add_page(page, name)
	
	def switch_front_page_to(self, page_name):
		"""
		Affiche la page associée au nom donné après avoir masqué l'actuelle
		"""

		self.pages[self.current_page].grid_remove()

		self.pages[page_name].grid()

		self.current_page = page_name
		
