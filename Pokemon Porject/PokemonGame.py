from PokemonTypes import Pokemon
from Player import UserPlayer
from Player import CompPlayer
from consolemenu import *
from consolemenu.items import *
import os 
clear = lambda: os.system('cls')
menu = SelectionMenu([''])

menu.get_selection(['Play'],title='Welcome to Zack\'s Pokemon Game!',show_exit_option=False)

user = UserPlayer()
comp = CompPlayer()

user.askPokemon(3)
comp.askPokemon(3,user.getNames())
menu.get_selection(['Fight!'],title='Your opponent has chosen their Pokemon',show_exit_option=False)
num = 1
while not(user.isDefeated()) and not(comp.isDefeated()):
    if num == 1:
        user.takeTurn(comp.getCurrentPokemon())
        num = 0
    else:
        comp.takeTurn(user.getCurrentPokemon())
        num = 1

if user.isDefeated():
    menu.get_selection(['Quit'],title='You lost! Your opponent won!',show_exit_option=False)
else:
    menu.get_selection(['Quit'],title='You Won! You beat your opponent!',show_exit_option=False)

