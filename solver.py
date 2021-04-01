import common
#import logic
import graphics


def solve_grid(grid):
	"""
	Prends une grille de sudoku (objet) en argument et retourne la grille resolue (sous forme d'objet)

	"""


	pass



def squares(grid):
	"""
	fait par Gabin Maury
	Prend une grille de sudoku (objet) et retourne une liste contenant 9 listes representant les differents carrés de 3x3 dans l'ordre
	"""
	def squarepos(x,y):
		"""
		Prends une position en argument et retourne le numero du carré (de 0 a 8)
		"""
		squarecoordx = str(row//3) #recupere la position x du carré actuel
		squarecoordy = str(column//3) #recupere la position y du carré actuel
		return int(squarecoordx + squarecoordy,base=3)#relie les deux positions (de 00 a 22), les considère comme un nombre en base 3 et les convertis en base 10 pour obtenir la bonne position de 0 a 8


	output = []
	for _ in range(len(grid)):
		output.append()
	for row in grille:
		for column in row:
			output[squarepos(row,column)].append(grid.get_number((row,column)))#on ajoute l'element actuel dans la bonne liste			
	return output


def rows(grid):
	return grid.grid

def columns(grid):
	"""
	for _ in range(9):
		output.append()
	for row in grid.grid:
		i = 0
		for column in row:
			i+=1
	"""

	#return [[grid[i][k] for k in range(9)] for i in range(9)] #a tester

