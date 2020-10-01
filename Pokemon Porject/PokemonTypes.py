from abc import ABC, abstractmethod



class Pokemon(ABC):
    pType = None
    maxHealth = None
    health = None
    attackPower = None
    weakAgainst = None

    def __init__(this,pokemonType):
        this.pType = pokemonType
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
    
    @abstractmethod
    def setType():
        pass

    @abstractmethod
    def setAttack():
        pass

    @abstractmethod
    def getAttacks():
        pass




