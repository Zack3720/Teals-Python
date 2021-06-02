import numpy as np
import os
import PySimpleGUI as sg
from random import randint

clear = lambda: os.system('cls')
clear()

board = np.array(['1','2','3','4','5','6','7','8','9'])
straights = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

def print_board():
    global board
    for i in range(3):
        print(board[(0+i*3):(3+i*3)])

def game_ended():
    global straights
    global board
    board_full = True
    for x in board:
        if x != 'O' and x != 'X':
            board_full = False
    if board_full:
        return 'draw'
    for winning_row in straights:
        if board[winning_row[0]] == board[winning_row[1]] and board[winning_row[0]] == board[winning_row[2]]:
            return board[winning_row[0]]
    return False
    
def valid_play(play):
    global board
    if board[play] == 'X' or board[play] == 'O':
        return False
    return True

def find_possible_straights(mark):
    global board
    global straights
    possible_straights = []
    for straight in straights:
        for x in range(3):
            if valid_play(straight[x%3]) and valid_play(straight[(x+1)%3]) and straight[(x+2)%3] == mark:
                possible_straights.append(straight)
                break
    return possible_straights


def make_play(turn):
    global board
    global straights
    opponent = ''
    # determinds what mark the opponent is.
    if turn == 'X':
        opponent = 'O'
    else:
        opponent = 'X'
    
    # Checks to see if we first have 2 marks in a row and then if we can play there
    # if we do we return it and win the game, else we check to see if the opponent
    # has 2 marks in a row and to see if we can block them.
    for mark in [turn,opponent]:
        for winning_row in straights:
            for x in range(3):
                if board[winning_row[x%3]] == board[winning_row[(x+1)%3]] and valid_play(winning_row[(x+2)%3]) and board[winning_row[x%3]] == mark:
                    return winning_row[(x+2)%3]


    #We are now assuming that the AI and Opponent both dont have a 2 in a row that can be blocked

    #Counting marks for the AI and Opponent
    my_count = 0
    opponent_count = 0
    for x in board:
        if x == turn:
            my_count += 1
        elif x == opponent:
            opponent_count += 1
    if my_count == 0 and opponent_count == '0':
        # This means the AI gets first move
        # Return random corner
        possible_moves = [0,2,6,8]
        return possible_moves[randint(0,3)]
    elif opponent_count > my_count:
        # This means opponent got first move

        # Checking overlaps
        opponent_straights = find_possible_straights(opponent)
        overlaps = []
        for current_straight in opponent_straights:
            for current_mark in straight:
                if not valid_play(current_mark):
                    continue
                if current_mark in overlaps:
                    continue
                for straight in opponent_straights:
                    if straight == current_straight:
                        continue
                    for mark in straight:
                        if current_mark == mark:
                            overlaps.append(current_mark)
                            break
                    if current_mark in overlaps:
                        break
        # After determining if there are any overlaping straights it will
        # block them, if the middle position overlaps with straights it will
        # choose that place to move, else it will choose the first overlap
        # There should only be one overlap if the middle is not overlaping.
        if 4 in overlaps:
            return 4
        elif len(overlaps) != 0:
            return overlaps[0]
        if opponent_count == 1:
            # This means the opponent just took their first 
            
            # If they went in corner I go middle
            # 0,2,6,8 -> 4
            sides = [1,3,5,7]
    else:
        return
        # This means the AI got first move
        
    

layout =  [
    [
        sg.Text('X\'s Turn',key='Text')
    ],
    [
        sg.Button(str(0*3+j+1), size=(8, 4), key=(0*3+j), pad=(0,0)) for j in range(3)
    ],
    [
        sg.Button(str(1*3+j+1), size=(8, 4), key=(1*3+j), pad=(0,0)) for j in range(3)
    ],
    [
        sg.Button(str(2*3+j+1), size=(8, 4), key=(2*3+j), pad=(0,0)) for j in range(3)
    ]
]

window = sg.Window('TicTacToe', layout)

twoplayer = True
turn = 'X'
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if not (game_ended() == False):
        continue

    if valid_play(event):
        window[event].update(turn, button_color=('white','black'))
        board[event] = turn
    else:
        window['Text'].update('Invaid Move')
        continue

    if game_ended() == turn:
        window['Text'].update(turn + ' Wins')
        continue
    elif game_ended() == 'draw':
        window['Text'].update('No Winners!')
        continue    
    else:
        if twoplayer:
            if turn == 'X':
                turn = 'O'
            else:
                turn = 'X'
        window['Text'].update(turn + '\'s turn!')
    #else:
        #AI Number Asking
window.close()
