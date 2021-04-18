"""
Module par Guilian Celin-Davanture
Module auxiliaire pour graphics.
"""


class Theme:
	"""
	Un theme possede:
		un nom d'affichage
		un dict de couleurs
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



def frame(theme):
	"""
	Renvoie un dict des paramètres appropriés
	pour une frame utilisant ce theme
	
	syntaxe : tk.Frame(master, **theme.frame(/le theme/) )
	"""
	return {
		'background' : theme.color_scheme['background']
	}

def button(theme):
	"""
	Renvoie un dict des paramètres appropriés
	pour un bouton utilisant ce theme

	syntaxe : tk.Button(master, **theme.button(/le theme/) )
	"""
	return {
		'background'         : theme.color_scheme['button_normal'],

		'activebackground'   : theme.color_scheme['button_pressed'],
		'activeforeground'   : theme.color_scheme['button_pressed_fg'],

		'disabledforeground' : theme.color_scheme['button_disabled_fg']
		}

def label(theme):
	"""
	Renvoie un dict des paramètres appropriés
	pour un label utilisant ce theme

	syntaxe : tk.Label(master, **theme.label(/le theme/) )
	"""
	return {
		'background' : theme.color_scheme['background'], 
		'foreground' : theme.color_scheme['primary_light']
		} 




#Valeurs "constantes" : permet d'acceder à Themes.GREY directement, sans classes ou enum ou autre diablerie.

DEFAULT = Theme(
		theme_name="Délicieux Défaut", 
		colors={
			'primary_light'     :  '#FFF',
			'primary_dark'      :  '#e4e6f1', 

			'secondary_light'   :  '#1e1e1e',
			'secondary_dark'    :  '#000',

			'background'        :  '#1e1e1e',

			'button_normal'     :  '#c47e1c',
			'button_pressed'    :  '#141414',
			'button_pressed_fg' :  '#FFF',

			'button_disabled'   :  '#1e1e1e',
			'button_disabled_fg':  '#FFF'
			} 
		)



"""

#Pour l'instant, les themes sont abandonnés.


GREY = Theme(
		theme_name="Gris tumultueux", 
		colors={
			'primary_light': '#FFF',
			'primary_dark':  '#d2dae2'
			}
		)

GREEN = Theme(
		theme_name="Emeraude etincelant", 
		colors={
			'primary_light': '#3edc81',  
			'primary_dark':'#0eac51'
			}
		)
BLUE = Theme(
		theme_name="Saveur bleutée", 
		colors={
			'primary_light': '#afc6ff', 
			'primary_dark':'#0097e6'
			}
		)
RED = Theme(
		theme_name="Rouge romantique", 
		colors={
			'primary_light': '#FDA7DF',
			'primary_dark':'#ff4750' 
			}
		)


"""