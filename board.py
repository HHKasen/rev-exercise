from enum import Enum
import numpy


#for spaces and players
class Space(Enum):
    EMPTY = 0
    BLACK = -1
    WHITE = 1

def space_invert(space):
    if(space==Space.BLACK):
        return Space.WHITE
    elif(space==Space.WHITE):
        return Space.BLACK
    else:
       raise ValueError("Error: Input not Space enum")

    
BRD_DIM = 8

def inbounds(ii):
    return (ii<BRD_DIM) and (ii>=0)

class Board():

    def __init__(self):
        self.board =  [[Space.EMPTY for _ in range(BRD_DIM)] for _ in range(BRD_DIM)]
        self.board[3][3] = Space.BLACK
        self.board[3][4] = Space.WHITE
        self.board[4][3] = Space.WHITE
        self.board[4][4] = Space.BLACK
        self.turn = Space.WHITE

    def game_over(self):
        """check if game is over in this state"""

        ws,bs = self.score()
        
        go_score = (ws+bs == 64) or (ws==0 or bs==0)

        #now if there are no legal moves for wither side, 
        go_moves = (len(self.legal_moves())==0) \
                    and ( len(self.legal_moves_turnless(space_invert(self.turn)))==0) 
        return go_score or go_moves

        
    def score(self):
        """
        gets current score of the board

        returns tuple of (white score, black score)
        """
        white_score = 0
        black_score = 0
        for ii in range(BRD_DIM):
            for jj in range(BRD_DIM):
                if(self.board[ii][jj]==Space.WHITE):
                    white_score += 1
                elif(self.board[ii][jj]==Space.BLACK):
                    black_score += 1
        return (white_score,black_score)        


    
    def legal_moves(self):
       """ Check for legal moves 

        for each empty space, do the following in each direction:
            check if adjacent piece in this direction is opposite color.
            if so, keep looking in that direction until we are out of bounds/empty
            if we see a player color piece, valid move

        """
       return self.legal_moves_turnless(self.turn)
       
    def legal_moves_turnless(self,turn):
        
        player_color = turn
        opp_color = space_invert(player_color)
        
        move_list = []
        dir_list = [ [1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
        
        for ii in range(BRD_DIM):
            for jj in range(BRD_DIM):
                if( self.board[ii][jj] == Space.EMPTY):
                    found = False
                    for (di,dj) in dir_list:
                        if( inbounds(ii+di) and inbounds(jj+dj) and self.board[ii+di][jj+dj]==opp_color):
                            ii_s,jj_s = ii+2*di,jj+2*dj
                            searching = True
                            while( inbounds(ii_s) and inbounds(jj_s) and searching):
                                if( self.board[ii_s][jj_s]==player_color):
                                    found = True
                                    searching = False
                                elif( self.board[ii_s][jj_s]==Space.EMPTY):
                                    searching = False
                                ii_s,jj_s = ii_s+di,jj_s+dj
                        if(found):
                            move_list.append( [ii,jj] )
                            break
                        
                            #print(ii,jj,"viable")
                        #if(found):
                            
        return move_list

    def place_piece(self,move):
        """
        places a piece on the board
        assumes that legality, turn being valid are already taken care of

        """

        if(move==None):
            pass

        else:
            ii,jj = move
            
            player_color = self.turn
            opp_color = space_invert(player_color)
            dir_list = [ [1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]

            self.board[ii][jj] = player_color

            for (di,dj) in dir_list:
                ii_s,jj_s = ii+di,jj+dj
                searching = True
                found = False
                #print("dir",di,dj)
                while( inbounds(ii_s) and inbounds(jj_s) and searching):
                    #print(ii_s,jj_s,self.board[ii_s][jj_s])
                    if( self.board[ii_s][jj_s]==player_color):
                        found = True
                        searching = False
                        #print("FOUND")
                    elif( self.board[ii_s][jj_s]==Space.EMPTY):
                        searching = False
                    else:
                        ii_s,jj_s=ii_s+di,jj_s+dj

                    if(found):
                        #print("found",di,dj)

                        for m in range( max(abs(ii_s-ii),abs(jj_s-jj))):
                            #print(m)
                            self.board[ii + m*di][jj + m*dj] = player_color

        self.turn = space_invert(self.turn)

    def __eq__(self,other):
        return ( (self.board==other.board) and (self.turn==other.turn) )
    def __repr__(self):

        ret_str = "  \u250F\u2501\u2501\u2501" + "\u2533\u2501\u2501\u2501"*7 + "\u2513"

        for ii in range(BRD_DIM):
            str_now = "\n" + str(8-ii)+ " \u2503"
            for jj in range(BRD_DIM):
                if(self.board[ii][jj]==Space.EMPTY):
                    str_now += "   \u2503"
                if(self.board[ii][jj]==Space.BLACK):
                    #str_now += "\u26AA \u2503"
                    str_now += " \u25CB \u2503"
                    
                if(self.board[ii][jj]==Space.WHITE):
                    #str_now += "\u26AB \u2503"
                    str_now += " \u25CF \u2503"
            if(ii!=(BRD_DIM-1)):
                ret_str += str_now + "\n  \u2523\u2501\u2501\u2501" + "\u254B\u2501\u2501\u2501"*7 + "\u252B"
        ret_str += str_now + "\n  \u2517\u2501\u2501\u2501" + "\u253B\u2501\u2501\u2501"*7 + "\u251B"
        ret_str += "\n    A   B   C   D   E   F   G   H"
        return ret_str

class Reversi():
    def __init__(self,board,w_player,b_player):
        self.board = board
        self.w_player = w_player
        self.b_player = b_player
        self.last_move_pass = False #used to track end of game due to conseq. passes
        self.game_over = False
        
    def resolve_turn(self):
        """ 
        Let a player take a turn, check if its eog, report score
        """

        if(self.board.turn == Space.WHITE):
            cand_move = self.w_player.choose_move(self.board)
        elif(self.board.turn == Space.BLACK):
            cand_move = self.b_player.choose_move(self.board)
        else:
            #raise error
            raise Exception("invalid turn")


        ##assert move in legal moves, or None
        ##should also check against legal moves
        ##
        ##

        legal_mvs = self.board.legal_moves()
        if( (cand_move==None and len(legal_mvs)>0) or (cand_move not in legal_mvs and len(legal_mvs)>0)  ): #This is slow, maybe flag for check?
            print(cand_move)
            print(legal_mvs,len(legal_mvs)>0)
            raise ValueError("Error: submitted pass when there were legal moves")

        #if(cand_move == None):            
            #if(len(self.board.legal_moves())>0): #This is slow, maybe flag for check?  
            #if(self.last_move_pass):
                #self.game_over=True
            #else:
                #self.board.place_piece(cand_move)
                #self.last_move_pass = True
        #else:
        self.board.place_piece(cand_move)
            #self.last_move_pass = False

        #after move, check if game is over
        #wscore, bscore = self.board.score()
        #if( (wscore+bscore==BRD_DIM**2) or (wscore==0) or (bscore==0)):
        self.game_over=self.board.game_over()


if __name__ == "__main__":
    print( "board eq test")

    board1 = Board()
    board2 = Board()

    print(board1==board2)

    board1.turn = Space.BLACK

    print(board1==board2)

    board1.turn = Space.WHITE
    board1.board[6][6] = Space.WHITE

    print(board1==board2)

    board2.board[6][6] = Space.WHITE
    print(board1==board2)
