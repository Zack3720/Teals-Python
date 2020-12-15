import datetime
import random
import sys
import os

clear = lambda: os.system('cls')
gameDate = datetime.date(1,3,1)
health = 5
food = 200
distanceLeft = 2000
name = 'Username'
healthReduced = 0
helpTyped = False


def help():
    print('List of actions \n')
    print('travel: moves you randomly between 30-60 miles and takes 3-7 days (random).')
    print('rest: increases health 1 level (up to 5 maximum) and takes 2-5 days (random).')
    print('hunt: adds 100lbs of food and takes 2-5 days (random).')
    print('status: lists food, health, distance traveled, and day.')
    print('help: lists all the commands.')
    print('quit: will end the game.\n')


def status():
    print('\n' + str(name) + '\'s stats! ')
    print('Food Remaining: ' + str(food) + 'lb.')
    print(str(name) + '\'s Health: ' + str(health) + '.')
    print('Distance to go: ' + str(distanceLeft) + ' miles.')
    print('Date: '+ str(gameDate.month)+'/'+str(gameDate.day)+'/'+str(gameDate.year + 1836)+'.')
    print('')

def travel():
    d = random.randint(3,7)
    m = random.randint(30,60)
    global distanceLeft
    passDays(d)
    distanceLeft -= m
    if distanceLeft <= 0:
        clear()
        startDate = datetime.date(1,3,1)
        daysPassed = gameDate - startDate
        print('\nYou win! You have successfully crossed The Oregon Trail!')
        print('It took you ' + str(daysPassed.days) + ' days to cross the orgeon trail')
        input("Press Enter to continue...")
        sys.exit()
    print('You have traveled ' + str(m) + ' miles!\n')
    
def rest():
    global health
    if health == 5:
        print("You are already at max health!\n")
        return
    d = random.randint(2,5)
    health += 1
    passDays(d)
    print('Your health has increased by 1!\n')

def hunt():
    d = random.randint(2,5)
    global food
    passDays(d)
    food += 100
    print('You gained 100lb of food!\n')

def passDays(d):
    global gameDate
    global healthReduced
    global food
    global health
    m = gameDate.month

    if d <= 0:
        print("You must rest for atleast one day!")
        return
    elif d is 1:
        print(str(d) + ' Days have passed!')
    else:
        print(str(d) + ' Days have passed!')
    delta = datetime.timedelta(days = d)
    gameDate = gameDate + delta
    food  -= 5*d

    if gameDate.month != m:    
        healthReduced = 0

    if healthReduced != 2 and (random.randint(0,int((31*(healthReduced+1)-gameDate.day)/(d*5)) == 0)):
        health -= 1
        healthReduced += 1
        if health == 0:
            print("\nYou died!")
            input("Press Enter to continue...")
            sys.exit()
        print('Your health has reduced by 1!')

    if food <= 0:
        food = 0
        health -= 1
        if health == 0:
            print("\nYou died due to malnutrition!")
            input("Press Enter to continue...")
            sys.exit()
        print('You lost 1 health because your out of food!')

    if gameDate.year != 1:
        print("\nGame Over! You took too long to cross The Oregon Trail and died in the winter!")
        input("Press Enter to continue...")
        sys.exit()

def readChat():
    global helpTyped
    while True:
        if not helpTyped: 
            print('Type \'help\' for a list of commands')
        helpTyped = False
        a = input('What do you wish to do? \n')
        args = a.split(' ')
        args[0] = args[0].lower()
        clear()
        if args[0] == "quit":
            sys.exit() 
        elif args[0] == 'help':
            help()
            helpTyped = True
        elif args[0] == 'status':
            status()
        elif args[0] == 'travel':
            travel()
        elif args[0] == 'rest':
            rest()
        elif args[0] == 'hunt':
            hunt()
        else:
            print('Thats not a valid command! \n')

def main():
    clear()
    global name
    name = input("What is your name?\n")
    clear()
    readChat()

if __name__ == "__main__":
    main()
