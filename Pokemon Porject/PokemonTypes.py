from abc import ABC, abstractmethod
import os

clear = lambda: os.system('cls')

pokemonDictionary = {
    'grass' : {
        'attacks' : {
            'Leaf Storm' : {
                'power' : 130,
                'accuracy' : 90,
            },
            'Mega Drain' : {
                'power' : 50,
                'accuracy' : 100,
            },
            'Razor Leaf' : {
                'power' : 55,
                'accuracy' : 95,
            }
        },
        'types' : {
            'Bulbasoar' : {
                'HP' : 60,
                'AP' : 40,
            },
            'Bellsprout' : {
                'HP' : 40,
                'AP' : 60,
            }, 
            'Oddish' : {
                'HP' : 50,
                'AP' : 50,
            }
        },
        'weak against' : 'fire'
    },
    'fire' : {
        'attacks' : {
            'Ember' : {
                'power' : 60,
                'accuracy' : 100,
            },
            'Fire Punch' : {
                'power' : 85,
                'accuracy' : 80,
            },
            'Flame Wheel' : {
                'power': 70,
                'accuracy' : 90,
            }
        },
        'types' : {
            'Charmainder' : {
                'HP' : 25,
                'AP' : 70,
            },
            'Ninetails' : {
                'HP' : 30,
                'AP' : 50,
            },
            'Ponyta' : {
                'HP' : 40,
                'AP' : 60,
            }
        },
        'weak against' : 'water'
    },
    'water' : {
        'attacks' : {
            'Bubble' : {
                'power' : 40,
                'accuracy' : 100,
            },
            'Hydro Pump' : {
                'power' : 185,
                'accuracy' : 30,
            },
            'Surf' : {
                'power' : 70,
                'accuracy' : 90,
            }
        },
        'types' : {
            'Squirtle' : {
                'HP' : 80,
                'AP' : 20,
            },
            'Psyduck' : {
                'HP' : 70,
                'AP' : 40,
            },
            'Polyway' : {
                'HP' : 50,
                'AP' : 50,
            }
        },
        'weak against' : 'grass'
    }
}

class Pokemon():
    pType = None
    pElement = None
    maxHealth = None
    health = None
    attackPower = None
    weakAgainst = None

    def __init__(this,pokemonElement,pokemonType):
        if pokemonDictionary[pokemonElement] == None:
            raise ValueError('Pokemon element is invalid')
        if pokemonDictionary[pokemonElement]['type'][pokemonType] == None:
            raise ValueError('Pokemon type is invalid') 
        this.pElement = pokemonElement
        this.pType = pokemonType
        maxHealth = pokemonDictionary[pokemonElement]['types'][pokemonType]['HP']
        health = maxHealth
        attackPower = pokemonDictionary[pokemonElement]['types'][pokemonType]['AP']
        weakAgainst = pokemonDictionary[pokemonElement]['weak against']
        super().__init__

    
    def attack(this, pokemon1, damage):
        pokemon1.takeDamage(damage, this.pType)
    
    def heal(this):
        this.health += 20

    
    def takeDamage(this, damage, aType):
        if this.weakAgainst == aType:
            this.health -= damage * 1.5
        else:
            this.health -= damage
        
        if this.health 
    
    
    def setType(this, pokemonType,):
        if pokemonDictionary['water']['type'][pokemonType] == None:
            raise ValueError('Pokemon type is invalid') 
        this.pType = pokemonType

    
    def setAttack():
        pass

    
    def getAttacks():
        pass

class GrassPokemon(Pokemon):
    global grassDictionary
    
    def __init__():
        super().__init__

    def setType(this,pokemonType):
        if pokemonDictionary['grass']['type'][pokemonType] == None:
            raise ValueError('Pokemon type is invalid') 
        this.pType = pokemonType

class FirePokemon(Pokemon):
    global fireDictionary

    def __init__():
        super().__init__

    def setType(this,pokemonType):
        if pokemonDictionary['fire']['type'][pokemonType] == None:
            raise ValueError('Pokemon type is invalid') 
        this.pType = pokemonType

class WaterPokemon(Pokemon):
    global pokemonDictionary

    def __init__():
        super().__init__

    def setType(this,pokemonType):
        if pokemonDictionary['water']['type'][pokemonType] == None:
            raise ValueError('Pokemon type is invalid') 
        this.pType = pokemonType

    def getType(this):
        return this.pType