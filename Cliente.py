import socketio
import random
from board import *
from minimax import *

username = 'Paul Belches'
tournament = 999999
tiempo = 0
tiros = 2
#Create socket
sio = socketio.Client()
#Conect to address
sio.connect('http://3.12.129.126:4000')
#sio.connect('http://localhost:4000')
#sio.connect('http://a2c47dd95c96.ngrok.io')

@sio.event
def connect():
    ## join in signal
    sio.emit('signin', {
        'user_name' : username,
        'tournament_id' : tournament,
        'user_role' : 'player'
    })
    #print("User : " + username + 'connected to tournament '  + tournament)

@sio.event
def ready(data):
    global tiros
    global tiempo

    #if (tiempo > 1.15):
    #    tiros -= 1
    print("Enemigo")
    print(humanBoard(data['board']))
    #try:
    move, tiempo = minimaxPrep(data['board'], data['player_turn_id'],  tiros)
    #print(move)
    #except:
    #move, tiempo = minimaxPrepNP(data['board'], data['player_turn_id'],  tiros)
    #tiempo = 10000000
    #print("Falle")

    #if (tiempo < 0.01):
    #    tiros += 1

    print(tiempo, tiros)
    print("Yo")
    print(move)
    print(move[0],move[1])
    data['board'][move[0]][move[1]] = 0
    print(humanBoard(data['board']))

    sio.emit('play', {
        'player_turn_id' : data['player_turn_id'],
        'tournament_id' : tournament,
        'game_id' : data['game_id'],
        'movement': [move[0],move[1]]
    })

@sio.event
def finish(data):
    print("Game finished")
    global tiros
    tiros = 2
    #Message to start again
    sio.emit('player_ready', {
        'tournament_id' : tournament,
        'game_id' : data['game_id'],
        'player_turn_id': data['player_turn_id']
    })

@sio.event
def disconnect():
    print("Connection to server closed!")

@sio.event
def ok_signin():
    print("Sign in succesful!")

@sio.event
def error_signin(data):
    print('error signing in')



