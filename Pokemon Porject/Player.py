from abc import ABC, abstractmethod
from PokemonTypes import Pokemon
from consolemenu import *
from consolemenu.items import *
import random
import os

clear = lambda: os.system('cls')
menu = SelectionMenu([''])

class Player(ABC):

    def __init__(self):
        super.__init__


    @abstractmethod
    def takeTurn(self):
        pass

    @abstractmethod
    def askPokemon(self):
        pass

    @abstractmethod
    def attack(self):
        pass
    
    def heal(self):
        self.currentPokemon.heal()

    @abstractmethod
    def switch(self):
        pass

    def getCurrentPokemon(self):
        return self.currentPokemon

    def getPokemonList(self):
        return self.pokemonList

    def isDefeated(self):
        if len(self.pokemonList) == 0:
            return True
        else:
            return False

class CompPlayer(Player):

    def __init__(self):
        super.__init__
        self.pokemonList = []
        self.currentPokemon = None
        self.hasPokemon = False
    
    def takeTurn(self,opponent: Pokemon):
        if not(self.hasPokemon):
            raise ValueError('Player has no Pokemon!')
        global menu

        if self.currentPokemon.getIsDead():
            self.pokemonList.pop(self.pokemonList.index(self.currentPokemon))
            if not(self.isDefeated()):
                self.switch()
            return


        if random.randint(0,2) <= 1:
            action = 0
        elif random.randint(0,1) == 1 or len(self.pokemonList) < 1:
            action = 1
        else:
            action = 2

        if action == 0:
            menu.get_selection(['Ok'],title='Your opponent chooses to attack!',show_exit_option=False)
            self.attack(opponent)
        elif action == 1:
            menu.get_selection(['Ok'],title='Your opponent chooses to heal!',show_exit_option=False)
            self.heal()
        elif action == 2:
            self.switch()

    def askPokemon(self, pokemonAmount,takenPokemon = []):

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
            selectedPokemon = list(pDict)[random.randint(0,len(pDict)-1)]
            self.pokemonList.append(Pokemon(pDict[selectedPokemon]['element'],selectedPokemon))
            pDict.pop(selectedPokemon)
        self.hasPokemon = True
        self.switch(False)

    def attack(self, opponent: Pokemon):
        global menu
        attackDict = self.currentPokemon.getAttacks()


        selectedAttack = random.randint(0,len(attackDict)-1)
        attack = list(attackDict)[selectedAttack]
        if self.currentPokemon.attack(opponent,attack):
            if opponent.getIsDead():
                menu.get_selection(['Ok'],title='Your opponent killed your '+opponent.getType()+'!',show_exit_option=False)
            else:
                menu.get_selection(['Ok'],title='Your opponent\'s attack landed!', subtitle='Your '+opponent.getType()+' now has '+str(opponent.getHealth())+'HP',show_exit_option=False)
        else:
            menu.get_selection(['Ok'],title='Their attack missed!',show_exit_option=False)

    def switch(self,displayMessage = True):
        selectedIndex = random.randint(0,len(self.pokemonList)-1)

        self.currentPokemon = self.pokemonList[selectedIndex] 
        if displayMessage:
            menu.get_selection(['Ok'],title='Your opponent switch to '+self.pokemonList[selectedIndex].getType()+'!',show_exit_option=False)

class UserPlayer(Player):
    pokemonNames = []
    
    def __init__(self):
        super.__init__
        self.pokemonList = []
        self.currentPokemon = None
        self.hasPokemon = False

    def takeTurn(self,opponent: Pokemon):
        if not(self.hasPokemon):
            raise ValueError('Player has no Pokemon!')

        global menu
        if self.currentPokemon.getIsDead():
            self.pokemonList.pop(self.pokemonList.index(self.currentPokemon))
            self.pokemonNames.pop(self.pokemonNames.index(self.currentPokemon.getType()))
            if not(self.isDefeated()):
                self.switch()
            return
        
        choosenAction = False
        while not(choosenAction):
            if len(self.pokemonList) > 1:
                action = menu.get_selection(['Attack','Heal','Switch','Your Pokemon\'s Stats'], title='Choose Action!',subtitle=('Opponent: ' + opponent.getType() + ' HP: ' + str(opponent.getHealth())), show_exit_option=False)
            else:
                action = menu.get_selection(['Attack','Heal','Your Pokemon\'s Stats'], title='Choose Action!',subtitle=('Opponent: ' + opponent.getType() + ' HP: ' + str(opponent.getHealth())), show_exit_option=False)
                if action == 2:
                    action += 1
            if action == 3:
                pString = ''
                for p in self.pokemonNames:
                    pString = pString + ' ' + p
                menu.get_selection(['Ok'],subtitle='Your Current Pokemon: '+self.currentPokemon.getType()+' HP: '+str(self.currentPokemon.getHealth())+' Element: '+self.currentPokemon.getElement(),title='List of Your Pokemon: '+pString,show_exit_option=False)
            else:
                choosenAction = True
        
        if action == 0:
            self.attack(opponent)
        elif action == 1:
            self.heal()
            menu.get_selection(['Ok'],title='You have healed you '+self.currentPokemon.getType()+'!',show_exit_option=False)
        elif action == 2:
            self.switch()

    def askPokemon(self, pokemonAmount,takenPokemon = []):
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
                    self.pokemonList.append(Pokemon(pDict[selectedPokemon]['element'],selectedPokemon))
                    self.pokemonNames.append(selectedPokemon)
                    pDict.pop(selectedPokemon)
        self.hasPokemon = True
        self.switch()
        
    def attack(self, opponent: Pokemon):
        global menu
        attacks = []
        attackDict = self.currentPokemon.getAttacks()

        for x in attackDict:
            attacks.append(str(x) + ' Power: ' + str(attackDict[x]['power']) + ' Accuracy: ' + str(attackDict[x]['accuracy']))

        selectedAttack = menu.get_selection(strings=list(attacks),title='Choose attack to use!',show_exit_option=False)
        attack = list(attackDict)[selectedAttack]
        if self.currentPokemon.attack(opponent,attack):
            if opponent.getIsDead():
                menu.get_selection(['Ok'],title='You have killed your opponent\'s '+opponent.getType()+'!',show_exit_option=False)
            else:
                menu.get_selection(['Ok'],title='Your attack landed!', subtitle='Your opponent\'s '+opponent.getType()+' now has '+str(opponent.getHealth())+'HP',show_exit_option=False)
        else:
            menu.get_selection(['Ok'],title='Your attack missed!',show_exit_option=False)

    def switch(self):
        global menu

        selectedIndex = menu.get_selection(strings=self.pokemonNames,title='Choose a Pokemon!',show_exit_option=False)

        self.currentPokemon = self.pokemonList[selectedIndex]

    def getNames(self):
        return self.pokemonNames 
