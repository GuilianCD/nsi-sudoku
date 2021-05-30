import time

import common
import logic
import database

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

def solve_grid_v2(grid, current_pos=0, debug=False):
	"""
	Va résoudre la grille en modifiant les cases.
	Renvoie True si la grille à été résolue.

	Par Guilian Celin-Davanture
	"""

	if current_pos == 81:
		#On est à la fin de la grille, au 82ème élément, qui n'existe pas
		return True

	#On obtient la position (x;y) de la position linéaire
	y = current_pos // grid.size
	x = current_pos % grid.size

	#On passe si la case est immuable
	if grid.is_immutable((x, y)):
		return solve_grid_v2(grid, current_pos + 1)

	for i in range(1, 10):
		#On essaye tout les chiffres de 1 à 9
		#Si il est possible d'insérer <i> ici:
		if is_num_possible(grid,x,y,i):
			grid.set_number((x,y),i)

			if debug:
				print(current_pos)
				show_grid(grid, current_pos)

				time.sleep(0.3)

			#On rappelle la fonction ici, en avancant le curseur
			res = solve_grid_v2(grid, current_pos + 1)

			if not res:
				# la récursion à renvoyé False, donc il y a un blockage
				# plus loin à cause d'une erreur faite ici ou plus haut,
				# donc on essaye un autre chiffre
				continue
			else:
				# Normalement impossible, mais au cas où
				return True

	# On réinitialise la case, pour éviter des blockages avant
	grid.set_number((x,y), None)

	# Et on renvoie False, signifiant le blockage.
	return False


def show_grid(grid, current=-1):
	"""
	Affiche la grille dans la ligne de commande
	de manière sympa :D

	Par Guilian celin-Davanture
	"""
	result = ""

	y1 = current // grid.size
	x1 = current % grid.size

	for y in range(grid.size):
		for x in range(grid.size):
			num = grid.get_number((x, y))

			if current != -1 and x == x1 and y == y1:
				result += '|'
			else:
				result += ' '

			result += "◙" if num is None else str(num)
			if current != -1 and x == x1 and y == y1:
				result += '|'
			else:
				result += ' '

		result += '\n'

	print(result)

if __name__ == '__main__':
	grid = database.fetch_random_grid_with_difficulty('moyenne')
	grid = grid[1]
	grid = logic.text_to_grid(grid)
	
	show_grid(grid)

	print(solve_grid_v2(grid))

	show_grid(grid)

#SAMPLE TEXT