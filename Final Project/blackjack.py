import PySimpleGUI as sg
from PIL import Image
import random
import time

path = 'Final Project\Images\Resized\\'
card_path = lambda card_name : path + card_name + '.png'

def shuffle(deck):
    shuffled_deck = []
    for x in range(len(deck)):
        shuffled_deck.append(deck.pop(random.randint(0,len(deck)-1)))
    return shuffled_deck

def create_deck(deck_size):
    suits = ['S','C','H','D']
    types = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    deck = []
    for s in suits:
        for t in types:
            deck.append(t+s)
    deck = deck*deck_size
    return shuffle(deck)

def hand_value(cards):
    aces = 0
    value = 0
    for c in cards:
        card = c[0:-1]
        if card.isnumeric():
            value += int(card)
        elif card == 'A':
            aces += 1
        else:
            value += 10
    if 21-value >= 11 and aces >= 1:
        value += aces + 10
    else:
        value += aces
    return value

def resize_card(card_name,size):
    image = Image.open('Final Project\Images\\' + card_name + '.png')
    resized = image.resize(size)
    resized.save(path + card_name + '.png')

def resize_cards(card_list,size):
    for card_name in card_list:
        resize_card(card_name,size)
    
def resize_game(cards_num,isPlayer = True):
    factor = (3/cards_num)
    if factor >= 1:
        return
    new_size = (int(size[0]*factor),int(size[1]*factor))
    if isPlayer:
        resize_cards(player_cards,new_size)
    else:
        resize_cards(dealer_cards,new_size)
    for x in range(cards_num):
        if isPlayer:
            window['P'+str(x)].update(size=new_size,filename=card_path(player_cards[x]))
        else:
            window['D'+str(x)].update(size=new_size,filename=card_path(dealer_cards[x]))
    window.Refresh()

def clear_board():
    global player_cards
    global dealer_cards
    global player_value
    global dealer_value
    global discard
    discard = player_cards.copy() + dealer_cards.copy()
    player_cards = []
    dealer_cards = []
    player_value = 0
    dealer_value = 0
    for x in range(11):
        s = (1,1) if x>1 else size
        resize_card('green',s)
        window['D'+str(x)].update(filename=card_path('green'),size=s)
        window['P'+str(x)].update(filename=card_path('green'),size=s)
    window['deal'].update(visible=True)
    window['bet'].update(visible=True)
    window.Refresh()

def update_bet():
    window['bet_text'].update('Bet: '+str(bet))
    window['cash'].update('Cash: '+str(cash))

def popup_window(txt):
    layout = [
        [sg.Text(txt)],
        [sg.Image(pad=(0,10))],
        [sg.Button('Ok')]
    ]
    PWindow = sg.Window('Pop-up',layout).Finalize()
    PWindow.Read()
    PWindow.Close()

sg.theme('DarkGreen5')

size = (100,150)

sidebar_layout = [
    [sg.Text('Cash: 100', background_color='Grey',size=(10,1),key='cash')],
    [sg.Image(pad=(0,100))],
    [sg.Button('Double Down',size=(10,1),key='double',visible=False)],
    [sg.Button('Deal',size=(10,1),key='deal')],
    [sg.Button('Hit',size=(10,1),key='hit',visible=False)],
    [sg.Button('Stay',size=(10,1),key='stay',visible=False)]
]

gameboard_layout = [
    [sg.Image(size=size if x<3 else (0,0),pad=(0,0),key='D'+str(x)) for x in range(11)],
    [sg.Image(pad=(1,10),visible=False)],
    [sg.Image(size=size if x<3 else (0,0),pad=(0,0), key='P'+str(x)) for x in range(11)]
    ]

title_layout = [
    [sg.Image(filename='Final Project\Images\Blackjack.png')],
    [sg.Button('Play',key='title-play',pad=(250,0),size=(10,1))]
]

buttonList = ['<<','<','0','>','>>']
bet_buttons = [
    [sg.Button(x,size=(5,2),pad=(0,0),key='bet_' + x) for x in buttonList]
]
game_layout = [
    [sg.Column(gameboard_layout),sg.Column(sidebar_layout)],
    [sg.Text('Bet:',key='bet_text',size=(19,1))],
    [sg.Column(bet_buttons,key = 'bet')]
]

layout = [
    [sg.Column(title_layout,key='title'),sg.Column(game_layout,visible=False,key='game')]
]

window = sg.Window('Black Jack', layout).Finalize()

deck = create_deck(2)
bet = 0
cash = 100
discard = []
dealer_cards = []
player_cards = []
dealer_value = 0
player_value = 0

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'title-play':
        window['title'].update(visible=False)
        window['game'].update(visible=True)
        window.set_min_size((370, 397))
    if event == 'deal':
        window['deal'].update(visible=False)
        window['bet'].update(visible=False)
        window['hit'].update(visible=True)
        window['stay'].update(visible=True)
        window['double'].update(visible=True)
        resize_card('back',size)
        for x in range(4):
            card = deck.pop(0)
            if x%2 == 0:
                player_cards.append(card)
            else:
                dealer_cards.append(card)
            resize_card(card,size)
            window[('P' if x%2 == 0 else 'D') + ('0' if x<2 else '1')].update(filename=card_path(card if not(x==1) else 'back'),size=size)
            window.refresh()
            time.sleep(0.1)
        player_value = hand_value(player_cards)
        dealer_value = hand_value(dealer_cards)
        if player_value == 21:
            if dealer_value != 21:
                popup_window('Natural! \n You won $' + str(bet*1.5) +'!')
                clear_board()
                cash += 2.5*bet
                bet = 0
                update_bet()
    if event == 'double':
        window['double'].update(visible=False)
        if cash >= bet*2:
            bet+= bet
            cash -= bet
        update_bet()
        event = 'hit'
    if event == 'hit':
        if player_value == 0:
            continue
        card = deck.pop(0)
        resize_card(card,size)
        window['P'+str(len(player_cards))].update(filename=card_path(card),size=size,visible=True)
        player_cards.append(card)
        resize_game(len(player_cards))
        player_value = hand_value(player_cards)
        if player_value > 21:
            popup_window('You went over! \n You lost $' + str(bet) + '.')
            bet = 0
            clear_board()
    if event == 'stay':
        if player_value == 0:
            continue
        resize_card(dealer_cards[0],size)
        window['D0'].update(filename=card_path(dealer_cards[0]))
        dealer_value = hand_value(dealer_cards)
        time.sleep(0.5)
        while True:
            if dealer_value <= 16:
                card = deck.pop(0)
                resize_card(card,size)
                window['D'+str(len(dealer_cards))].update(filename=card_path(card),size=size,visible=True)
                dealer_cards.append(card)
                resize_game(len(dealer_cards),False)
                dealer_value = hand_value(dealer_cards)
                window.Refresh()
                time.sleep(0.5)
            else:
                break
        if dealer_value > 21:
            popup_window('The dealer goes over! \n You won $' + str(bet) + '.')
            cash += 2*bet
            bet = 0
        elif dealer_value > player_value:
            popup_window('The dealer beat you! \n You lost $' + str(bet)+ '.')
            bet = 0
        elif dealer_value < player_value:
            popup_window('You beat the dealer! \n You won $' + str(bet)+'.')
            cash += 2*bet
            bet = 0
        elif dealer_value == player_value:
            popup_window('You push!')
            cash += bet
            bet = 0
        update_bet()
        clear_board()
    if event.startswith('bet_'):
        event = event.replace('bet_','')
        if event == '<<':
            if bet <= 10:
                cash += bet
                bet = 0
            else:
                cash += 10
                bet -= 10
        elif event == '<':
            if bet <= 5:
                cash += bet
                bet = 0
            else:
                cash += 5
                bet -= 5
        elif event == '0':
            cash += bet
            bet = 0
        elif event == '>':
            if cash >= 5:
                cash -= 5
                bet += 5
        elif event == '>>':
            if cash >= 10:
                cash -= 10
                bet += 10
        update_bet()