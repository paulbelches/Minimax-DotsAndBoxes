import copy
import time
from board import *
import numpy as np
from numba import jit
movement = []

@jit    
def evaluation(tablero):
    return np.sum(np.where(tablero == 99, 0, tablero))

#def evaluation(tablero):
#    c = 0
    ##Probablemente , pasar a numpy
#    for i in range(len(tablero[0])):
        #pasar a numpy
#        if (tablero[0][i] != 99 and tablero[0][i] != 0):
#            c += tablero[0][i]
#        if (tablero[1][i] != 99 and tablero[1][i] != 0):
#            c += tablero[1][i]
#    return c

def posibleMovements(tablero, player):
    posibles = []
    #Pasar a threads
    #print("Tablero recibido", tablero)
    #tablero = copy.deepcopy(tablero)
    #print("Largo del tablero recibifo", len(tablero[0]))
    for i in range(len(tablero[0])):
        if (tablero.item(0,i) == 99):
            #print("Entre")
            tablero[0][i] = cuadro(tablero, 0, i, player)
            t = ( copy.deepcopy(tablero), (0,i) )
            posibles.append(t)
            tablero[0][i] = 99
        if (tablero.item(1,i) == 99):
            tablero[1][i] = cuadro(tablero, 1, i, player)
            t = ( copy.deepcopy(tablero), (1,i) )
            posibles.append(t)
            tablero[1][i] = 99
    return posibles
    
@jit
def cuadro(position, r, t, player):
    a = t
    c = 0
    if (r == 0):
        y = a // 6
        if (a % 6 != 0):
            if (position[0][a - 1] != 99 and 
                position[1][6 * (a-(6*y) - 1) + y] != 99 and 
                position[1][6 * (a-(6*y) - 1) + y + 1] != 99):
                c += player
                #print("if 1")
            #print(a, a-1, 6 * (a-(6*y) - 1) + y,  6 * (a-(6*y) - 1) + y + 1, "----", 
            #    position[0][a], 
            #    position[0][a-1], 
            #    position[1][6 * (a-(6*y) - 1) + y],  
            #    position[1][6 * (a-(6*y) - 1) + y + 1])
        if ( a % 6 != 5):
            if (position[0][a + 1] != 99 and 
                position[1][6 * (a-(6*y)) + y] != 99 and 
                position[1][6 * (a-(6*y)) + y + 1]  != 99):
                c += player
                #print("if 2")
            #print( a, a+1, 6 * (a-(6*y)) + y,  6 * (a-(6*y)) + y + 1, "----", 
            #    position[0][a], 
            #    position[0][a+1], 
            #    position[1][6 * (a-(6*y)) + y],  
            #    position[1][6 * (a-(6*y)) + y + 1]) 
    else:
        y = a // 6
        if (a % 6 != 0):
            if ( position[1][a - 1] != 99 and 
                 position[0][6 * (a-(6*y) - 1) + y] != 99 and 
                 position[0][6 * (a-(6*y) - 1) + y + 1] != 99):
                c += player
                #print("if 3")
            #print(a, a-1, 6 * (a-(6*y) - 1) + y,  6 * (a-(6*y) - 1) + y + 1, "----", 
            #    position[1][a], 
            #    position[1][a - 1], 
            #    position[0][6 * (a-(6*y) - 1) + y], 
            #    position[0][6 * (a-(6*y) - 1) + y + 1])
        if ( a % 6 != 5):
            if (position[1][a + 1] != 99 and 
                position[0][6 * (a-(6*y)) + y] != 99 and 
                position[0][6 * (a-(6*y)) + y + 1]  != 99):
                c += player
                #print("if 4")
            #print( a, a+1, 6 * (a-(6*y)) + y,  6 * (a-(6*y)) + y + 1, "----", 
            #    position[1][a],
            #    position[1][a + 1],
            #    position[0][6 * (a-(6*y)) + y], 
            #    position[0][6 * (a-(6*y)) + y + 1])
    return c
@jit
def gameOver(position):
    return np.sum(position[0]) < 99 and np.sum(position[1]) < 99
    #return not(99 position[0]) and not(99 in position[1])

@jit
def max(a,b):
    if (a>b):
        return a
    else:
        return b

@jit
def min(a,b):
    if (a<b):
        return a
    else:
        return b

def minimax(position, depth, alpha, beta, maximizingPlayer, moves, lstCall):
    if (depth == 0 or gameOver(position)):
        return (evaluation(position) ,moves, lstCall)
    tMoves = []
    anwserMoves = (0,0)
    anwserCalls = []
    presentValue = evaluation(position)
    #Max
    if (maximizingPlayer):
        maxEval = float('-inf')
        tlstCall = copy.deepcopy(lstCall)
        tlstCall.append("Max")
        #if (len(posibleMovements(position, 1)) == 0):
        #    print("Aaaaaaaaaaaaaaa")
        #    print(posibleMovements(position, 1))
        for child in posibleMovements(position, 1):
            #Agregar movimiento anterior
            tMoves = copy.deepcopy(moves)
            tMoves.append(child[1])
            if ( (evaluation(child[0]) - presentValue) > 0 ):
                eval = minimax(child[0], depth, alpha, beta, True, tMoves, tlstCall)
            else:
                eval = minimax(child[0], depth - 1, alpha, beta, False, tMoves, tlstCall)

            if ( eval[0] > maxEval ):
                maxEval = eval[0]
                anwserMoves = eval[1]
                anwserCalls = eval[2]

            alpha = max(eval[0], alpha)

            if (beta <= alpha):
                break

        return (maxEval, anwserMoves, anwserCalls)
    #Min
    else:
        minEval = float('inf')
        tlstCall = copy.deepcopy(lstCall)
        tlstCall.append("Min")
        for child in posibleMovements(position, -1):
            #Agregar movimiento anterior
            tMoves = copy.deepcopy(moves)
            tMoves.append(child[1])
            if ( (evaluation(child[0]) - presentValue) < 0 ):
                eval = minimax(child[0], depth, alpha, beta, False, tMoves, tlstCall)
            else:
                eval = minimax(child[0], depth - 1, alpha, beta, True, tMoves, tlstCall)

            if ( eval[0] < minEval ):
                minEval = eval[0]
                anwserMoves = eval[1]
                anwserCalls = eval[2]

            beta = min(eval[0], beta)

            if (beta <= alpha):
                break

        return (minEval, anwserMoves, anwserCalls)
    
def minimaxPrep(board, turnId, tiros):
    start = time.time()
    boardNP = np.matrix(board)
    if (turnId == 2):
        boardNP = boardNP * -1
        boardNP = np.where(boardNP == -99, 99, boardNP)
    else:
        boardNP = boardNP * 1
        boardNP = np.where(boardNP == -99, 99, boardNP)
        #print(boardNP)
        #for i in range(len(board[0])):
        #    if (board[0][i] != 99):
        #        board[0][i] = -1 * board[0][i]
        #    if (board[1][i] != 99):
        #        board[1][i] = -1 * board[1][i]
    #print(boardNP)
    #print("tiros", tiros)
    move = minimax(boardNP, tiros, float('-inf'), float('inf'), True, [], [])
    #print("Movimiento", move)
    end = time.time()
    return move[1][0],  end - start

"""
board = [
    [0,  0, 99, 99, 99, 99,
     99,  99, 99, 99, 99, 99,
     99,  99, 99, 99, 99, 99,
     99,  99, 99, 99, 99, 99,
     99,  99, 99, 99, 99, 99
    ],
    [ 0, 99, 99, 99, 99, 99,
     99, 99, 99, 99, 99, 99,
     99, 99, 99, 99, 99, 99, 
     99, 99, 99, 99, 99, 99, 
     99, 99, 99, 99, 99, 99
    ]

]
"""
"""
board = [
    [0,  99, 0, 0, 0, 0,
     0,  99, 0, 0, 0, 0,
     99,  99, 99, 99, 99, 99,
     99,  99, 99, 99, 99, 99,
     99,  99, 99, 99, 99, 99
    ],
    [ 0, 99, 0, 0, 0, 0,
      0, 99, 0, 0, 0, 0,
      99, 99, 0, 99, 99, 99, 
      99, 99, 99, 99, 99, 99, 
      99, 99, 99, 99, 99, 99
    ]

]
"""
"""
board = [
    [-99, -1, -2, -3, -4,
     -5, -6, -7, -8, -9,
     -10, -11, -12, -13, -14,
     -15, -16, -17, -18, -19,
     -20, -21, -22, -23, -24,
     -25, -26, -27, -28, -29
    ],
    [0, 1, 2, 3, 4,
     5, 6, 7, 8, 9,
     10, 11, 12, 13, 14,
     15, 16, 17, 18, 19,
     20, 21, 22, 23, 24,
     25, 26, 27, 28, 29
    ]
]"""

#anw = minimax(board, 2, float('-inf'), float('inf'), True, [], [])

#print(humanBoard(board))

#print( anw )
#pythoprint( anw[1] )

#print(cuadro(board, 1, 13, 1))

#sboard[anw[1][0][0]][anw[1][0][1]] = 0

#print(humanBoard(board))

#print(cuadro(board, 0, 1, 1))
#print(posibleMovements(np.matrix(board), -1))
#print(board[1][20], board[1][21], board[0][15], board[0][16])
#print(cuadro(board, 1, 14, 1))

#print(cuadro(np.matrix(board0), 1, 1, 1))

#print(evaluation(board))

#print()
#print(minimax(board, 2, float('-inf'), float('inf'), True, [], []))#

#print(cuadro(board, 1, 13, 1))