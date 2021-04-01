"""
Module par Guilian Celin-Davanture
Module auxiliaire pour graphics.
"""

class Theme:
	"""
	Un theme possede:
		un nom d'affichage
		un tuple de couleurs
	"""

	

	def __init__(self, theme_name, colors):
		"""
		colors est un tuple
		"""
		super(Theme, self).__init__()
		self.colors = colors
		self.theme_name = theme_name

	@property
	def color(self):
		return self.colors

	@property
	def name(self):
		return self.theme_name


class Themes:
	"""
	docstring for Themes
	"""

	def __new__(self):
		self._themes = {
			"GRIS":  Theme(theme_name="Gris tumultueux", colors=('#d1ccc0', '#FFF')),
			"BLEU":  Theme(theme_name="Saveur bleutée", colors=('#0097e6', '#afc6ff')),
			"ROUGE": Theme(theme_name="Rouge romantique", colors=('#ff4750', '#FDA7DF')) #WIP
		}

	def __getattr__(self, name):
		return self._themes[name]