"""
Module par Guilian Celin-Davanture

Module d'utilitaires pour graphics, pour
alléger le module.
"""

from tkinter import *

import theme as Themes

class RowCounter():
	"""
	Une classe qui permet d'incrémenter automatiquement une variable
	Cette classe à été créée car la même fonction était répétée trois fois déja
	"""
	def __init__(self, base=0):
		self.counter = base

	def next(self):
		"""
		Renvoie le prochain indice
		"""
		self.counter += 1
		return self.counter - 1

class BetterEntry():
	"""
	Cette classe permet d'avoir un widget Entry avec des capacités améliorées,
	comme la possibilité d'avoir un texte de remplacement quand il n'y a rien
	d'écrit par l'utilisateur.
	"""
	def __init__(self, master, placeholder_text, is_password=False, width=0, placeholder_color="#5c5c5c", text_color="#000"):
		"""
		master est le widget qui sera le parent
		placeholder_text est le texte a afficher quand il n'y a rien d'écrit et
		que le widget n'as pas le focus
		is_password définit si des * seront affichés quand l'utilisateur écrit.
		"""
		if width == 0:
			self.widget = Entry(master)
		else:
			self.widget = Entry(master, width=width)
		
		self.placeholder_color = placeholder_color
		self.text_color = text_color

		self.placeholder = placeholder_text

		self.is_password = is_password

		#Quand on clique sur l'entry, si le texte est le placeholder, elle va enlever le placeholder
		self.widget.bind("<FocusIn>", lambda e : self.clear_placeholder())
		#Si il n'y a rien d'écrit, écrit le placeholder.
		self.widget.bind("<FocusOut>", lambda e : self.set_placeholder())

		self.set_placeholder()

	def clear_placeholder(self):
		if self.widget.get() == self.placeholder: #Si le texte est différent du placeholder, c'est un texte entré par l'utilisateur.
			if self.is_password:
				self.widget.config(show='*')
			self.widget.config(foreground=self.text_color)
			self.widget.delete(0, END)

	def set_placeholder(self):
		if self.widget.get(): #Si il y a du texte, l'utilisateur a entré quelque chose
			return
		self.widget.config(show='')
		self.widget.config(foreground=self.placeholder_color)
		self.widget.insert(0, self.placeholder)

	def get(self):
		return self.widget.get()

class ScrollableFrame():

	def __init__(self, master, width, height, grid_row=0, grid_col=0, space_inbetween_elements=0, **kwargs):
		"""
		Une ScrollableFrame est une frame pouvant défiler (seulement verticalement !).

		grid_row et grid_col sont les paramètres qui seront passés à grid() de ce "widget",
		car il s'affiche tout seul.

		space_inbetween_elements est la marge qui séparera deux éléments dans la liste,
		en pixels.
		"""
		#Le container est la frame qui contiendra l'autre frame, cette dernière étant celle qui va défiler
		self.container = Frame(master, width=width, height=height, **kwargs)
		self.container.grid()
		self.container.grid_propagate(0)

		self.scrollable = Frame(self.container, width=width, **kwargs)

		self.contained = list()
		

	def add_item(self, item):
		"""
		Cette fonction ajoute l'item à la liste des éléments contenus dans le menu défilant.
		"""
		self.contained.append(item)

	@property
	def widget(self):
		"""
		Appeler cette priorité pour obtenir le widget
		a utiliser comme parent dans l'architecture
		tkinter.
		"""
		return self.scrollable


	def __getattr__(self, attr):
		"""
		Si l'on appelle par exemple ScrollableFrame.grid(), il y aurait
		normalement une erreur : ici on empêche cette erreur en passant
		si besoin l'attribut du même nom du container.
		"""
		return getattr(self.container, f'{attr}')