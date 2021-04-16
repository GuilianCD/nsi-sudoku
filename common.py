"""
Module par Guilian Celin-Davanture
"""

import random


class SudokuGrid:
	"""
	Représente une grille de sudoku de dimensions variables.
	Donne acces a des methodes pour changer l'etat de chaque case
	La grille est initialisee pleine de None
	"""
	def __init__(self, size = 9, premade_grid=[]):
		"""
		Fournir un tableau bidimensionnel de valeurs et de None
		à cette fonction résultera en une grille initialisée avec
		les valeurs immuables (celles définissant cette grille de
		sudoku) placés aux valeurs et None aux autres

		Donner par exemple
		[
			[ 1,    None, None ],
			[ None, 0,    4],
			[ None, 6,    None]
		]
		résultera en une grille où l'on ne peut pas changer
		les valeurs des ici 1, 0, 4 et 6.
		"""
		super(SudokuGrid, self).__init__()
		self._size = size

		if not premade_grid:
			self._grid = []

			#Genere la grille vide
			for _ in range(size):
				ll = []
				for _ in range(size):
					#Ici, on utilise un dictionnaire au lieu d'une simple valeur 
					#car certaines cases de la grille sont immuables (sinon, le
					#joueur pourrait supprimer les nombres qui l'embête et faire
					#une toute autre grille). Le tag 'immutable' indique ici qu'on
					#ne peut pas changer ce nombre.
					number = {'value': None, 'immutable': False}
					ll.append(number)

				self._grid.append(ll)
		else:
			newgrid = []

			for array in premade_grid:
				newarray = []
				for number in array:
					is_immutable = not (number is None)
					newarray.append({'value': number, 'immutable': is_immutable})
				newgrid.append(newarray)

			self._grid = newgrid

	@property
	def grid(self):
		"""
		Renvoie la grille interne comme elle serait si on 
		ne stockait que des valeurs et pas un dictionnaire
		"""
		grid = self._grid
		newgrid = []

		for array in grid:
			new_array = []
			for number in array:
				new_array.append(number['value'])
			newgrid.append(new_array)

		return newgrid

	@property
	def true_grid(self):
		"""
		Renvoie la grille interne
		"""
		return self._grid

	@property
	def size(self):
		"""
		Renvoie la taille de la grille interne
		"""
		return self._size

	@grid.setter
	def grid(self, newgrid):
		"""
		Donne une nouvelle valeur a la grille interne
		"""
		self._grid = newgrid 

	def is_immutable(self, pos):
		x, y = pos 
		return self._grid[x][y]['immutable']

	def set_number(self, pos, value):
		x, y = pos 

		if not self._grid[x][y]['immutable']:
			self._grid[x][y]['value'] = value
			return 0
		else:
			return -1

	def get_number(self, pos):
		x, y = pos
		return self._grid[x][y]['value']



def get_random_title():
	"""
	Renvoie un titre de fenetre aleatoire dans la liste predetermine.
	"""

	#organisé de façcon suivante :
	#"titre" : poids (chance d'obtenir)
	#Le poids équivaut à un coefficient
	titles = {
		"Sudoku" : 20,
		"Minecraft" : 7,
		"Sudoku 2 (Maintenant avec 0% de viande humaine)" : 5,
		"Sudoku 2 (avec 100% de viande humaine..?)" : 4,
		"Ceci n'est pas un titre de fenêtre." : 6, #Magritte
		"[object Object]" : 3,
		"print('Sudoku')" : 3,
		"""Exception in thread "main" java.lang.NullPointerException at com.oracle.sun.main(Main.java:31)""" : 5
	}

	#Cette liste contiendra tout les titres, le nombre de fois que le poids est
	#i.e. : "titre 1" avec un poids de 5, et "titre 2" avec un poids de 2, donnent :
	# ["titre 1", "titre 1", "titre 1", "titre 1", "titre 1", "titre 2", "titre 2"]
	#, ou "titre 1" 5 fois et "titre 2" 2 fois
	weighted_titles = list()

	weight_sum = 0
	for title, weight in titles.items():
		weight_sum += weight
		for _ in range(weight):
			weighted_titles.append(title)

	choice = round(random.random() * weight_sum) - 1 #Prends une valeur entière de 1 (inclu) à weight_sum (exclu)

	return weighted_titles[choice]
	








if __name__ == '__main__':
	from pprint import pprint

	gri = SudokuGrid(9)
	gri.set_number((0, 1), value=4)
	pprint(gri.grid)




		
