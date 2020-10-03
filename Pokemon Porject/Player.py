from abc import ABC, abstractmethod
from PokemonTypes import Pokemon
from consolemenu import *
from consolemenu.items import *
import os

clear = lambda: os.system('cls')
menu = SelectionMenu([''])

class Player(ABC):
    pokemonList = []
    currentPokemon = None
    hasPokemon = False

    def __init__(this):
        super.__init__

    @abstractmethod
    def takeTurn(this):
        pass

    @abstractmethod
    def askPokemon(this):
        pass

    @abstractmethod
    def attack(this):
        pass
    
    def heal(this):
        currentPokemon.heal()

    @abstractmethod
    def switch(this):
        pass

#class CompPlayer(Player):


class UserPlayer(Player):
    pokemonNames = []
    
    def __init__(this):
        super.__init__

    def takeTurn(this,opponent: Pokemon):
        if not(this.hasPokemon):
            raise ValueError('Player has no Pokemon!')

        global menu
        action = menu.get_selection(['Attack','Heal','Switch'], title='Choose Action!',subtitle=('Opponent: ' + opponent.getType() + ' HP: ' + opponent.getHealth()), show_exit_option=False)

        
        if action == 0:
            this.attack(opponent)
        elif action == 1:
            this.heal()
        elif action == 2:
            this.switch()

    def askPokemon(this, pokemonAmount):
        global menu 

        # Makes a nested dictionary 'pDict' that list all pokemon types
        # And adds their elements to their dictionary.
        pDict = {}
        eList = list(Pokemon.getPokemonDict().keys())
        for element in eList:
            temp = Pokemon.getPokemonDict()[element]['types']
            for t in temp:
                temp[t]['element'] = element
            pDict.update(temp)
        
        for x in range(pokemonAmount):
            pokemonSelected = False
            while not(pokemonSelected):
                selectedIndex = menu.get_selection(strings=list(pDict),title='Pokemon Selection',subtitle='Choose a pokemon to view it\'s stats',show_exit_option=False)
                selectedPokemon = list(pDict)[selectedIndex]
                if not(bool(menu.get_selection(strings=['Choose','Back'],title=selectedPokemon,subtitle=('AP: ' + str(pDict[selectedPokemon]['AP']) + '  HP: ' + str(pDict[selectedPokemon]['HP']) + '  Element: ' + pDict[selectedPokemon]['element']),show_exit_option=False))):
                    pokemonSelected = True
                    this.pokemonList.append(Pokemon(pDict[selectedPokemon]['element'],selectedPokemon))
                    this.pokemonNames.append(selectedPokemon)
        
    def attack(this, opponent):
        global menu
        attacks = []
        attackDict = this.currentPokemon.getAttacks()

        for x in attackDict:
            attacks.append(str(x) + ' Power: ' + attackDict[x]['power'] + 'Accuracy: ' + str(attackDict[x]['accuracy']))

        selectedAttack = menu.get_selection(string=list(attacks),title='Choose attack to use!',show_exit_option=False)

    def switch(this):
        global menu

        selectedIndex = menu.get_selection(strings=this.pokemonNames,title='Choose a Pokemon!',show_exit_option=False)

        this.currentPokemon = this.pokemonList[selectedIndex] 


print('Horray!')
