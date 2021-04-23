import PySimpleGUI as sg
from random import randint
import numpy
import time
from PIL import Image

#Returns true if the given play is valid on the given board
def valid_play(board, play):
    for i in range(6):
        if board[play][5-i] == ' ':
            return True
    else:
        return False

#Board: The board state to evalute
#Color: The player to evalute for. Higher the score the better for this player/color
#Next_turn: the next color to play
#Returns a score between -1(Player can lose next turn) to 1(Player can win next turn). Anything between those numbers is a approximation
#Of how good of chances the player has to win with that board. It is based off of how many 3 tile straights each player has and how many
#Tiles below them are empty.
def evaluate_board(board, color, next_turn):
    #Make a function to evaluate the state of a board and give it a 'grade'
    #0.035x^3 min -9 max 9
    #6-x
    scale = lambda a : (0.036*(a**3))/10
    player_winning_tiles = find_winning_tiles(board, color)
    opponent_winning_tiles = find_winning_tiles(board, 'R' if color == 'Y' else 'Y')
    #Only need one factor sum since the player factors are added to this while the opponents factors are subtracted
    winning_factors_sum = 0.0
    for tile in player_winning_tiles:
        tiles_below = find_tiles_below(board,tile)
        if next_turn == color and tiles_below == 0:
            return 1.0
        winning_factors_sum += scale(6-tiles_below)
    for tile in opponent_winning_tiles:
        tiles_below = find_tiles_below(board,tile)
        if next_turn != color and tiles_below == 0:
            return -1.0
        winning_factors_sum -= scale(6-tiles_below)
    #print(winning_factors_sum)
    return max(-0.9,min(0.9,winning_factors_sum))

#Returns number of empty tiles below a given tile.
#Tile is a tuple of lenth two (x,y)
def find_tiles_below(board,tile):
    #print('tile:' + str(tile))
    x = tile[0]
    y = tile[1]
    tile_counter = 0
    for i in range(5-y):
        #print(board[x][y+i])
        if board[x][y+i+1] == ' ':
            tile_counter += 1
        else:
            break
    return tile_counter

#Finds all of the 3 in a row tiles that are not blocked. Does not count 4 in a row tiles. Only checks one color
#Takes in:
#Board - Current board state to check
#Color - the color of tiles to check for.
def find_winning_tiles(board, color):
    #check all grey tiles if there is a three in a row by it.
    tiles = []
    for x,row in enumerate(board):
        for y,value in enumerate(row):
            if value != ' ':
                continue

            if y>=3 and x>=3:
                for i in range(1,4):
                    if color != board[x-i][y-i]:
                        break
                else:
                    tiles.append((x,y))
                    continue
            if y>=3:
                for i in range(1,4):
                    if color != board[x][y-i]:
                        break
                else:
                    tiles.append((x,y))
                    continue
            if y>=3 and x<=3:
                for i in range(1,4):
                    if color != board[x+i][y-i]:
                        break
                else:
                    tiles.append((x,y))
                    continue
            if x<=3:
                for i in range(1,4):
                    if color != board[x+i][y]:
                        break
                else:
                    tiles.append((x,y))
                    continue
            if y<=2 and x<=3:
                for i in range(1,4):
                    if color != board[x+i][y+i]:
                        break
                else:
                    tiles.append((x,y))
                    continue
            if y<=2:
                for i in range(1,4):
                    if color != board[x][y+i]:
                        break
                else:
                    tiles.append((x,y))
                    continue
            if y<=2 and x>=3:
                for i in range(1,4):
                    if color != board[x-i][y+i]:
                        break
                else:
                    tiles.append((x,y))
                    continue
            if x>=3:
                for i in range(1,4):
                    if color != board[x-i][y]:
                        break
                else:
                    tiles.append((x,y))
                    continue
    return tiles

#Changes the pictures of given tile and refreshes the page window
#Takes in:
#x - x postion of tile
#y - y postion of tile
#filename - the filename for the picture to change it the tile to
def changePicture(x,y, filename):
    window[(x,y)].update(filename= filename)
    window.Refresh()

#Checks if game is over for the current board state
#Returns 3 values, true/false if game is over, the 4 tiles in a row that won the game, and the winning color
def is_game_over(board):
    gameOver = False
    for x,row in enumerate(board):
        for y,value in enumerate(row):
            if value == ' ':
                continue
            tiles = []
            #changePicture(x,y, filename= 'blackred.png' if value == 'R' else 'blackyellow.png')
            #time.sleep(.05)

            if y>=3 and x>=3:
                tiles.append((x,y))
                for i in range(1,4):
                    if value != board[x-i][y-i]:
                        tiles.clear()
                        break
                    tiles.append((x-i,y-i))
                else:
                    gameOver = True
                    break
            if y>=3:
                tiles.append((x,y))
                for i in range(1,4):
                    if value != board[x][y-i]:
                        tiles.clear()
                        break
                    tiles.append((x,y-i))
                else:
                    gameOver = True
                    break
            if y>=3 and x<=3:
                tiles.append((x,y))
                for i in range(1,4):
                    if value != board[x+i][y-i]:
                        tiles.clear()
                        break
                    tiles.append((x+i,y-i))
                else:
                    gameOver = True
                    break
            if x<=3:
                tiles.append((x,y))
                for i in range(1,4):
                    if value != board[x+i][y]:
                        tiles.clear()
                        break
                    tiles.append((x+i,y))
                else:
                    gameOver = True
                    break
            if y<=2 and x<=3:
                tiles.append((x,y))
                for i in range(1,4):
                    if value != board[x+i][y+i]:
                        tiles.clear()
                        break
                    tiles.append((x+i,y+i))
                else:
                    gameOver = True
                    break
            if y<=2:
                tiles.append((x,y))
                for i in range(1,4):
                    if value != board[x][y+i]:
                        tiles.clear()
                        break
                    tiles.append((x,y+i))
                else:
                    gameOver = True
                    break
            if y<=2 and x>=3:
                tiles.append((x,y))
                for i in range(1,4):
                    if value != board[x-i][y+i]:
                        tiles.clear()
                        break
                    tiles.append((x-i,y+i))
                else:
                    gameOver = True
                    break
            if x>=3:
                tiles.append((x,y))
                for i in range(1,4):
                    if value != board[x-i][y]:
                        tiles.clear()
                        break
                    tiles.append((x-i,y))
                else:
                    gameOver = True
                    break
            #changePicture(x,y, filename= 'red.png' if value == 'R' else 'yellow.png')
        if gameOver:
            return True, tiles, board[tiles[0][0]][tiles[0][1]]
    return False, None, ' '

#Takes in a board and a play and color of player then returns a copy of the board with the move played.
def make_play(board, play, color):
    new_board = []
    for x in board:
        new_board.append(x.copy())
    for i in range(6):
        if new_board[play][5-i] == ' ':
            new_board[play][5-i] = color
            return new_board
    else:
        return None

#Minmax to find the best move to play
#Parameters:
#Board - current board state to find play for
#Color - the color of the player to play for
#Next_turn - the color who plays next
#Depth - how many layers deep to check.
#
#Returns two values, the number of the best move it found and the 'confidence' level of the move. How well it 
#sees that move as.
def find_next_move(board, color, next_turn, depth):
    opponent_color = 'R' if color == 'Y' else 'Y'
    best_move = None
    best_score = None
    if color == next_turn:
        #Max
        for i in range(7):
            new_board = make_play(board,i,color)
            if new_board == None:
                continue
            if is_game_over(new_board)[0]:
                return i, 1
            elif depth > 0:
                _, move_score = find_next_move(new_board,color,'R' if next_turn == 'Y' else 'Y',depth-1)
                if best_move == None:
                    best_move = i
                    best_score = move_score
                elif best_score < move_score:
                    best_move = i
                    best_score = move_score
            else:
                move_score = evaluate_board(new_board,color,next_turn)
                if best_move == None:
                    best_move = i
                    best_score = move_score
                elif best_score < move_score:
                    best_move = i
                    best_score = move_score
        if best_score > 0:
            best_score -= 0.001
        elif best_score < 0:
            best_score += 0.001
        return best_move, best_score
    else:
        #Min
        for i in range(7):
            new_board = make_play(board,i,opponent_color)
            if new_board == None:
                continue
            if is_game_over(new_board)[0]:
                return i, -1
            elif depth > 0:
                _, move_score = find_next_move(new_board,color,'R' if next_turn == 'Y' else 'Y',depth-1)
                if best_move == None:
                    best_move = i
                    best_score = move_score
                elif best_score > move_score:
                    best_move = i
                    best_score = move_score
            else:
                move_score = evaluate_board(new_board,color,next_turn)
                if best_move == None:
                    best_move = i
                    best_score = move_score
                elif best_score > move_score:
                    best_move = i
                    best_score = move_score
        if best_score > 0:
            best_score -= 0.001
        elif best_score < 0:
            best_score += 0.001
        return best_move, best_score

#Returns a board with all empty values and changes the window's board to all grey
def clear_board(board):
    board = [[' ' for j in range(6)] for i in range(7)]
    for i in range(7):
        for j in range(6):
            window[i,j].update(filename='grey.png')
    return board

picture = 'Connectfour.png'
image = Image.open(picture)
temp = image.resize((250,50))
temp.save('temp.png')

MAX_COL = 7
size = 70

#Layout of the game window
layout2 =  [
    [
        sg.Button(int(j), size=(8, 2), key=(j), pad=(1,1)) for j in range(MAX_COL)
    ],
    [
        sg.Image(size=(size, size), key=(j,0), pad=(1,1), filename='grey.png') for j in range(MAX_COL)
    ],
    [
        sg.Image(size=(size, size), key=(j,1), pad=(1,1), filename='grey.png') for j in range(MAX_COL)
    ],
    [
        sg.Image(size=(size, size), key=(j,2), pad=(1,1), filename='grey.png') for j in range(MAX_COL)
    ],
    [
        sg.Image(size=(size, size), key=(j,3), pad=(1,1), filename='grey.png') for j in range(MAX_COL)
    ],
    [
        sg.Image(size=(size, size), key=(j,4), pad=(1,1), filename='grey.png') for j in range(MAX_COL)
    ],
    [
        sg.Image(size=(size, size), key=(j,5), pad=(1,1), filename='grey.png') for j in range(MAX_COL)
    ],
    [
        sg.Button('Back', key='Back'),sg.Image(key='--',visible=True,pad=(205,0)),sg.Button('Reset', key='Reset')
    ]
]

#Layout of the start menu
layout1 = [[sg.Image(filename='temp.png')],
           [sg.Button('1 Player', key='one_player', pad=(40,0)),sg.Button('2 Player', key='two_player', pad=(0,0))]]

#Combiens the layouts so one is always invisible. This is so we can switch between them.
layout = [[sg.Column(layout1, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-')]]

window = sg.Window('Connect 4', layout).Finalize()

board = [[' ' for j in range(6)] for i in range(7)]
game_over = False
one_player = True
turn = 'R'
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Reset':
        board = clear_board(board)
        game_over = False
        turn = 'R'
        continue
    if event == 'one_player':
        one_player = True
        window['-COL1-'].update(visible=False)
        window['-COL2-'].update(visible=True)
        continue
    if event == 'two_player':
        one_player = False
        window['-COL1-'].update(visible=False)
        window['-COL2-'].update(visible=True)
        continue
    if event == 'Back':
        window['-COL2-'].update(visible=False)
        window['-COL1-'].update(visible=True)
        turn = 'R'
        game_over = False
        board = clear_board(board)
        continue
    if game_over:
        continue
    #For some reason the zero button is getting the key '00' when it should be 0 so I catch the error here
    if event == '00':
        event = 0
    if one_player:
        for i in range(6):
            if board[int(event)][5-i] == ' ':
                window[(event,5-i)].update(filename= 'red.png' if turn == 'R' else 'yellow.png')
                window.Refresh()
                board[event][5-i] = turn
                turn = 'R' if turn == 'Y' else 'Y'
                game_over, tiles, winner = is_game_over(board)
                if game_over:
                    print(winner+ ' is the winner')
                    for tile_x,tile_y in tiles:
                        changePicture(tile_x,tile_y, filename= 'winred.png' if board[tile_x][tile_y] == 'R' else 'winyellow.png')
                    continue
                AI_move, value = find_next_move(board,turn,turn,4)
                print(value)
                for j in range(6):
                    if board[AI_move][5-j] == ' ':
                        window[(AI_move,5-j)].update(filename= 'red.png' if turn == 'R' else 'yellow.png')
                        board[AI_move][5-j] = turn
                        turn = 'R' if turn == 'Y' else 'Y'
                        break
                #print(evaluate_board(board,'R',turn))
                break
        else:
            print('invalid play')
    else:
        #Two player Code
        for i in range(6):
            if board[int(event)][5-i] == ' ':
                window[(event,5-i)].update(filename= 'red.png' if turn == 'R' else 'yellow.png')
                window.Refresh()
                board[event][5-i] = turn
                turn = 'R' if turn == 'Y' else 'Y'
                break
        else:
            print('invalid play')
    game_over, tiles, winner = is_game_over(board)
    if game_over:
        print(winner+ ' is the winner')
        for tile_x,tile_y in tiles:
            changePicture(tile_x,tile_y, filename= 'winred.png' if board[tile_x][tile_y] == 'R' else 'winyellow.png')
window.close()