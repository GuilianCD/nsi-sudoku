"""
Module par Guilian Celin-Davanture
Module auxiliaire pour graphics.
"""


class Theme:
	"""
	Un theme possede:
		un nom d'affichage
		un dict de couleurs
		ces couleurs sont :
			primary_light
			primary_dark
			(WIP)
	"""

	

	def __init__(self, theme_name, colors):
		"""
		colors est un dict
		"""
		super(Theme, self).__init__()
		self.colors = colors
		self.theme_name = theme_name

	@property
	def color_scheme(self):
		return self.colors

	@property
	def name(self):
		return self.theme_name


#Valeurs constantes : permet d'acceder à Themes.GREY directement, sans classes ou enum ou autre diablerie.

GREY = Theme(
		theme_name="Gris tumultueux", 
		colors={
			'primary_light': '#d1ccc0',
			'primary_dark':'#FFF'
			}
		)
BLUE = Theme(
		theme_name="Saveur bleutée", 
		colors={
			'primary_light': '#0097e6',
			'primary_dark':'#afc6ff'
			}
		)
RED = Theme(
		theme_name="Rouge romantique", 
		colors={
			'primary_light': '#ff4750',
			'primary_dark':'#FDA7DF'
			}
		)



"""
BLUE =  Theme(theme_name="Saveur bleutée", colors=('#0097e6', '#afc6ff'))
RED  =  Theme(theme_name="Rouge romantique", colors=('#ff4750', '#FDA7DF')) #WIP	
"""