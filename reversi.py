import random
import board
import enum
import os
from time import sleep
from basicPlayers import *
from mctsPlayer import MCTSPlayer,rollout    
        
        
if(__name__ == "__main__"):
    
    #white_player = HumanPlayer("White")
    white_player = MCTSPlayer("White")
    
    #black_player = MCTSPlayer("Black")
    #black_player = HumanPlayer("Black")
    black_player = RandomPlayer("Black")
    

    gb = board.Board()
    #if(True):
    #gb.board[2][2] = board.Space.WHITE
    #gb.board[1][1] = board.Space.WHITE
    #gb.board[5][5] = board.Space.BLACK
    #gb.board[6][6] = board.Space.BLACK
    
    
    rev_game = board.Reversi(gb,white_player,black_player)

    while(not rev_game.game_over):
    #for kk in range(1):
        os.system('clear')
        print(rev_game.board.turn)
        print(rev_game.board)    
        rev_game.resolve_turn()

    print(rev_game.board)


    
    #really crappy, gets implied game over. should handle more gracefully
    wscore,bscore = rev_game.board.score()

    if(wscore+bscore == 64):
        print("game over, no more empty spaces\n")
    elif(wscore==0 or bscore==0):
        print("game over, one side is eliminated\n")
    else:
        print("game over, no legal moves for either color\n")

    if(wscore>bscore):
        print("white wins, " + str(wscore) + " to " + str(bscore))
    elif(bscore>wscore):
        print("black wins, " + str(bscore) + " to " + str(wscore))
    else:
        print("the game is tied, "  + str(bscore) + " to " + str(wscore))

