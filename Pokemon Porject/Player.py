from abc import ABC, abstractmethod
from PokemonTypes import Pokemon
from consolemenu import *
from consolemenu.items import *
import random
import os

clear = lambda: os.system('cls')
menu = SelectionMenu([''])

class Player(ABC):

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
        this.currentPokemon.heal()

    @abstractmethod
    def switch(this):
        pass

    def getCurrentPokemon(this):
        return this.currentPokemon

    def getPokemonList(this):
        return this.pokemonList

    def isDefeated(this):
        if len(this.pokemonList) == 0:
            return True
        else:
            return False

class CompPlayer(Player):

    def __init__(this):
        super.__init__
        this.pokemonList = []
        this.currentPokemon = None
        this.hasPokemon = False
    
    def takeTurn(this,opponent: Pokemon):
        if not(this.hasPokemon):
            raise ValueError('Player has no Pokemon!')
        global menu

        if this.currentPokemon.getIsDead():
            this.pokemonList.pop(this.pokemonList.index(this.currentPokemon))
            if not(this.isDefeated()):
                this.switch()
            return


        if random.randint(0,2) <= 1:
            action = 0
        elif random.randint(0,1) == 1 or len(this.pokemonList) < 1:
            action = 1
        else:
            action = 2

        if action == 0:
            menu.get_selection(['Ok'],title='Your opponent chooses to attack!',show_exit_option=False)
            this.attack(opponent)
        elif action == 1:
            menu.get_selection(['Ok'],title='Your opponent chooses to heal!',show_exit_option=False)
            this.heal()
        elif action == 2:
            this.switch()

    def askPokemon(this, pokemonAmount,takenPokemon = []):

        # Makes a nested dictionary 'pDict' that list all pokemon types
        # And adds their elements to their dictionary.
        pDict = {}
        eList = list(Pokemon.getPokemonDict().keys())
        for element in eList:
            temp = Pokemon.getPokemonDict()[element]['types']
            toRemove = []
            for t in temp:
                if t in takenPokemon:
                    toRemove.append(t)
                else:
                    temp[t]['element'] = element
            for t in toRemove:
                temp.pop(t)
            pDict.update(temp)
        
        for x in range(pokemonAmount):
            if len(pDict) == 0:
                break
            pokemonSelected = False
            selectedPokemon = list(pDict)[random.randint(0,len(pDict)-1)]
            this.pokemonList.append(Pokemon(pDict[selectedPokemon]['element'],selectedPokemon))
            pDict.pop(selectedPokemon)
        this.hasPokemon = True
        this.switch(False)

    def attack(this, opponent: Pokemon):
        global menu
        attackDict = this.currentPokemon.getAttacks()


        selectedAttack = random.randint(0,len(attackDict)-1)
        attack = list(attackDict)[selectedAttack]
        if this.currentPokemon.attack(opponent,attack):
            if opponent.getIsDead():
                menu.get_selection(['Ok'],title='Your opponent killed your '+opponent.getType()+'!',show_exit_option=False)
            else:
                menu.get_selection(['Ok'],title='Your opponent\'s attack landed!', subtitle='Your '+opponent.getType()+' now has '+str(opponent.getHealth())+'HP',show_exit_option=False)
        else:
            menu.get_selection(['Ok'],title='Their attack missed!',show_exit_option=False)

    def switch(this,displayMessage = True):
        selectedIndex = random.randint(0,len(this.pokemonList)-1)

        this.currentPokemon = this.pokemonList[selectedIndex] 
        if displayMessage:
            menu.get_selection(['Ok'],title='Your opponent switch to '+this.pokemonList[selectedIndex].getType()+'!',show_exit_option=False)

class UserPlayer(Player):
    pokemonNames = []
    
    def __init__(this):
        super.__init__
        this.pokemonList = []
        this.currentPokemon = None
        this.hasPokemon = False

    def takeTurn(this,opponent: Pokemon):
        if not(this.hasPokemon):
            raise ValueError('Player has no Pokemon!')

        global menu
        if this.currentPokemon.getIsDead():
            this.pokemonList.pop(this.pokemonList.index(this.currentPokemon))
            this.pokemonNames.pop(this.pokemonNames.index(this.currentPokemon.getType()))
            if not(this.isDefeated()):
                this.switch()
            return
        
        choosenAction = False
        while not(choosenAction):
            if len(this.pokemonList) > 1:
                action = menu.get_selection(['Attack','Heal','Switch','Your Pokemon\'s Stats'], title='Choose Action!',subtitle=('Opponent: ' + opponent.getType() + ' HP: ' + str(opponent.getHealth())), show_exit_option=False)
            else:
                action = menu.get_selection(['Attack','Heal','Your Pokemon\'s Stats'], title='Choose Action!',subtitle=('Opponent: ' + opponent.getType() + ' HP: ' + str(opponent.getHealth())), show_exit_option=False)
                if action == 2:
                    action += 1
            if action == 3:
                pString = ''
                for p in this.pokemonNames:
                    pString = pString + ' ' + p
                menu.get_selection(['Ok'],subtitle='Your Current Pokemon: '+this.currentPokemon.getType()+' HP: '+str(this.currentPokemon.getHealth())+' Element: '+this.currentPokemon.getElement(),title='List of Your Pokemon: '+pString,show_exit_option=False)
            else:
                choosenAction = True
        
        if action == 0:
            this.attack(opponent)
        elif action == 1:
            this.heal()
            menu.get_selection(['Ok'],title='You have healed you '+this.currentPokemon.getType()+'!',show_exit_option=False)
        elif action == 2:
            this.switch()

    def askPokemon(this, pokemonAmount,takenPokemon = []):
        global menu 

        # Makes a nested dictionary 'pDict' that list all pokemon types
        # And adds their elements to their dictionary.
        pDict = {}
        eList = list(Pokemon.getPokemonDict().keys())
        for element in eList:
            temp = Pokemon.getPokemonDict()[element]['types']
            toRemove = []
            for t in temp:
                if t in takenPokemon:
                    toRemove.append(t)
                else:
                    temp[t]['element'] = element
            for t in toRemove:
                temp.pop(t)
            pDict.update(temp)
        
        for x in range(pokemonAmount):
            if len(pDict) == 0:
                break
            pokemonSelected = False
            while not(pokemonSelected):
                selectedIndex = menu.get_selection(strings=list(pDict),title='Pokemon Selection',subtitle='Choose a pokemon to view it\'s stats',show_exit_option=False)
                selectedPokemon = list(pDict)[selectedIndex]
                if not(bool(menu.get_selection(strings=['Choose','Back'],title=selectedPokemon,subtitle=('AP: ' + str(pDict[selectedPokemon]['AP']) + '  HP: ' + str(pDict[selectedPokemon]['HP']) + '  Element: ' + pDict[selectedPokemon]['element']),show_exit_option=False))):
                    pokemonSelected = True
                    this.pokemonList.append(Pokemon(pDict[selectedPokemon]['element'],selectedPokemon))
                    this.pokemonNames.append(selectedPokemon)
                    pDict.pop(selectedPokemon)
        this.hasPokemon = True
        this.switch()
        
    def attack(this, opponent: Pokemon):
        global menu
        attacks = []
        attackDict = this.currentPokemon.getAttacks()

        for x in attackDict:
            attacks.append(str(x) + ' Power: ' + str(attackDict[x]['power']) + ' Accuracy: ' + str(attackDict[x]['accuracy']))

        selectedAttack = menu.get_selection(strings=list(attacks),title='Choose attack to use!',show_exit_option=False)
        attack = list(attackDict)[selectedAttack]
        if this.currentPokemon.attack(opponent,attack):
            if opponent.getIsDead():
                menu.get_selection(['Ok'],title='You have killed your opponent\'s '+opponent.getType()+'!',show_exit_option=False)
            else:
                menu.get_selection(['Ok'],title='Your attack landed!', subtitle='Your opponent\'s '+opponent.getType()+' now has '+str(opponent.getHealth())+'HP',show_exit_option=False)
        else:
            menu.get_selection(['Ok'],title='Your attack missed!',show_exit_option=False)

    def switch(this):
        global menu

        selectedIndex = menu.get_selection(strings=this.pokemonNames,title='Choose a Pokemon!',show_exit_option=False)

        this.currentPokemon = this.pokemonList[selectedIndex]

    def getNames(this):
        return this.pokemonNames 
