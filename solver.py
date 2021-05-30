import common
import logic
import graphics

def is_num_possible(grid,x,y,num):
		"""
		Fait par Gabin Maury
		Prends une grille (objet), une position et un nombre et verifie si ce nombre est une entrée valide dans ces coordonnées de la grille.
		"""
		for i in range(9): 
			if grid.get_number((x, i)) == num: #Verifie si le nombre est dans la colonne
				return False
		for i in range(9):
			if grid.get_number((i, y)) == num: #Verifie si le nombre est dans la ligne
				return False
		square_list = logic.squares(grid)
		for number in square_list[logic.squarepos(x,y)]: #Verifie si le nombre est dans le carré
			if number == num:
				return False
		return True

def solve_grid(grid):
	"""
	Fait par Gabin Maury
	Prends une grille de sudoku (objet) en argument et resout la grille.

	"""
	for x in range(9):
		for y in range(9):
			if grid.get_number((x,y)) == None:
				for i in range(1,10):
					if is_num_possible(grid,x,y,i):
						grid.set_number((x,y),i)
						solve_grid(grid) #Recursivité
						grid.set_number((x,y), None) #Si cette branche de recursivité n'est pas bonne, alors remet None dans la case
				return #si aucune possibilité ne marche, on arrete la fonction (la branche de recursivité n'est pas bonne)


#SAMPLE TEXT