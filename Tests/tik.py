import numpy as np
import os

clear = lambda: os.system('cls')
clear()

board = np.array(['1','2','3','4','5','6','7','8','9'])

def print_board():
    global board
    for i in range(3):
        print(board[(0+i*3):(3+i*3)])

def game_ended():
    straights = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    global board
    if (len(np.where(board == 'X')) + len(np.where(board == 'O'))) == 9:
        return 'draw'
    for winning_row in straights:
        if board[winning_row[0]] == board[winning_row[1]] and board[winning_row[0]] == board[winning_row[2]]:
            return board[winning_row[0]]
    return ' '
    
def valid_play(play):
    global board
    if not play.isnumeric():
        print('Value must be a number between 1-9')
        return False
    if not (1 <= int(play) and int(play) <= 9):
        print('Value must be a number between 1-9')
        return False
    if board[int(play)-1] == 'X' or board[int(play)-1] == 'O':
        print('That position is already filled')
        return False
    return True

def game_place():
    global board
    while True:
        clear()
        while True:
            print_board()
            opp1 = input('Where to put your mark?[X] ')
            if valid_play(opp1):
                board[int(opp1)-1] = 'X'
                break
        if game_ended() == 'X':
            print('Opponent One Wins!')
            break
        elif game_ended() == 'draw':
            print('No Winner!')
            break
        clear()
        while True:
            print_board()
            opp2 = input('Where to put your mark?[O] ')
            if valid_play(opp2):
                board[int(opp2)-1] = 'O'
                break
        if game_ended() == 'O':
            print('Opponent Two Wins!')
            break
        elif game_ended() == 'draw':
            print('No Winner!')
            break
game_place()

