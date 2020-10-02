from PokemonTypes import Pokemon
from consolemenu import *
from consolemenu.items import *
import os 
clear = lambda: os.system('cls')

clear()

menu = SelectionMenu([''])

menu.get_selection(['Ok'],title='',show_exit_option=False)
