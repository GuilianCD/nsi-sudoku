
import random


class SudokuGrid:
	"""
	Représente une grille de sudoku de dimensions variables.
	Donne acces a des methodes pour changer l'etat de chaque case
	La grille est initialisee pleine de 0
	"""
	def __init__(self, size = 9):
		super(SudokuGrid, self).__init__()
		self._size = size
		self._grid = []

		#Genere la grille vide
		for _ in range(size):
			ll = []
			for _ in range(size):
				ll.append(None)
			self._grid.append(ll)

	@property
	def grid(self):
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

	def set_number(self, pos, value):
		x, y = pos
		self._grid[x][y] = value

	def get_number(self, pos):
		x, y = pos
		return self._grid[x][y]




def get_random_title():
	"""
	Renvoie un titre de fenetre aleatoire dans la liste predetermine.
	"""
	titles = [
	"Sudoku 2 (Maintenant sans pesticides !)",
	"Sudoku 2 (Maintenant avec 0% de viande humaine)",
	"Sudoku 2 (avec 100% de viande humaine..?)",
	"Minecraft",
	"????",
	"Je suis coince dans ce jeu, cliquez sur la croix en haut a droite pour me liberer !!1!1! svp !!! j'ai une femme et des enfants, je dois leur manquer terriblement !",
	"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
	"[REDACTED]",
	"[object Object]",
	"print('Sudoku')",
	'Exception in thread "main" java.lang.NullPointerException at com.oracle.sun.main(Main.java:31)' 
	]

	return random.choice(titles)






if __name__ == '__main__':
	from pprint import pprint

	gri = SudokuGrid(9)
	gri.set_number((0, 1), value=4)
	pprint(gri.grid)




		
