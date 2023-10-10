import board
from time import sleep
import random

class Player():
    def __init__(self,name):
        self.name = name
    
    def choose_move(self,board):
        """
        takes a board, and returns a move
        """
        pass
        return None

class RandomPlayer(Player):
    def choose_move(self,board):
        moves = board.legal_moves()

        #sleep(0.5)
        if(len(moves)>0):
            return random.choice(moves)
        else:
            return None
        
def mth_move(m_move):
    " converts move from 2-list to human read"
    return chr(65+m_move[1]) + str(8-m_move[0])
    
    
    

def htm_move(h_move):
    letters = ['A','B','C','D','E','F','G','H']
    numbers = ['1','2','3','4','5','6','7','8']

    
    if(len(h_move)!=2):
        return None
    else:
        letter,number = h_move
        if( (letter in letters) and (number in numbers) ):
            move = [8-int(number),ord(letter)-65]
            return move
        else:
            return None

    

class HumanPlayer(Player):
    def choose_move(self,board):
        moves = board.legal_moves()

        if(len(moves)>0):
            move_selected = False

            while( not move_selected):
                print( self.name + " to move. Legal moves:")

                for move in moves:
                    print( mth_move(move) + ",",end="")

                user_move = input("\nEnter your move:")

                if(htm_move(user_move)==None):
                    print("Sorry, I couldn't understand that.")
                elif(htm_move(user_move) not in moves):
                    print("Sorry, that move is not legal.")
                else:
                    v_move = htm_move(user_move)
                    move_selected = True
                    return v_move
        else:
            input( self.name + " to move. No legal moves, press enter to pass:")
            return None
        
    
