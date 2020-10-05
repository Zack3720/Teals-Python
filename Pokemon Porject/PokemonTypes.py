import random
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
        'strong against' : ['water']
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
        'strong against' : ['grass']
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
            'Polywag' : {
                'HP' : 50,
                'AP' : 50,
            }
        },
        'strong against' : ['fire']
    }
}

class Pokemon():
    pType = None
    pElement = None
    maxHealth = None
    health = None
    attackPower = None
    strongAgainst = None
    isDead = False

    def __init__(this,pokemonElement,pokemonType):
        try:
            pokemonDictionary[pokemonElement]
        except KeyError:
            raise ValueError('Pokemon element is invalid')
        try:
            pokemonDictionary[pokemonElement]['types'][pokemonType]
        except KeyError:
            raise ValueError('Pokemon type is invalid')
            
        this.pElement = pokemonElement
        this.pType = pokemonType
        this.maxHealth = pokemonDictionary[pokemonElement]['types'][pokemonType]['HP']
        this.health = this.maxHealth
        this.attackPower = pokemonDictionary[pokemonElement]['types'][pokemonType]['AP']
        this.strongAgainst = pokemonDictionary[pokemonElement]['strong against']

    def attack(this, opponent, attack):
        try:
            pokemonDictionary[this.pElement]['attacks'][attack]
        except KeyError:
            raise ValueError('Invalid attack for this Pokemon')
        
        attackUsed = pokemonDictionary[this.pElement]['attacks'][attack]

        if random.randint(0,100) < attackUsed['accuracy']:
            if this.attackPower > attackUsed['power']:
                opponent.takeDamage(attackUsed['power'], this.strongAgainst)
            else:
                opponent.takeDamage(this.attackPower, this.strongAgainst)
            return True
        else:
            return False
    
    def heal(this):
        this.health += 20
        if this.maxHealth < this.health:
            this.health = this.maxHealth

    def takeDamage(this, damage, strongAgainst):
        if (this.pElement in strongAgainst):
            this.health -= damage * 1.5
        else:
            this.health -= damage
            
        if this.health <= 0:
            this.isDead = True

    def getElement(this):
        return this.pElement

    def getType(this):
        return this.pType

    def getIsDead(this):
        return this.isDead

    def getHealth(this):
        return this.health
    
    def getAttacks(this):
        return pokemonDictionary[this.pElement]['attacks']

    @staticmethod
    def getPokemonDict():
        return pokemonDictionary
