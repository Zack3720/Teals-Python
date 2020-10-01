from abc import ABC, abstractmethod
import os

clear = lambda: os.system('cls')

attacks = {
    'grass' : {
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
    'fire' : {
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
    'water' : {
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
    }
}

pokemonTypes = {
    'grass' : {
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
    'fire' : {
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
    'water' : {
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
    }
}

class Pokemon(ABC):
    pType = None
    maxHealth = None
    health = None
    attackPower = None
    weakAgainst = None

    def __init__(this,pokemonType):
        this.pType = pokemonType
        super().__init__

    @abstractmethod
    def attack(this, pokemon1, damage):
        pokemon1.takeDamage(damage, this.pType)
    
    def heal(this):
        this.health += 20

    
    def takeDamage(this, damage, aType):
        if this.weakAgainst == aType:
            this.health -= damage * 1.5
        else:
            this.health -= damage
    
    @abstractmethod
    def setType():
        pass

    @abstractmethod
    def setAttack():
        pass

    @abstractmethod
    def getAttacks():
        pass

class GrassPokemon(Pokemon):
    
    def __init__(this,pokemonType):
        this.pType = pokemonType
        super().__init__

class FirePokemon(Pokemon):

    def __init__(this,pokemonType):
        this.pType = pokemonType
        super().__init__

class WaterPokemon(Pokemon):

    def __init__(this,pokemonType):
        this.pType = pokemonType
        super().__init__