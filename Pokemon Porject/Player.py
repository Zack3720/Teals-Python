from abc import ABC, abstractmethod
from PokemonTypes import Pokemon
from consolemenu.items import *
from consolemenu import *
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

class CompPlayer(Player):


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
        
        currentPokemon = pokemonList[menu.get_selection(strings=this.pokemonNames,title='')]
        

    def attack(this, opponent):
        pass

    def switch(this):
        pass


