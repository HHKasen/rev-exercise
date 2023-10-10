import board
from basicPlayers import *
import copy
import numpy as np
import random

#tunable params
N_iter = 2000 #number of iters to run each move
C_ex = 1 #magic number

class MCTSPlayer(Player):
    def __init__(self,name):
        super().__init__(name)
        self.root = None
        
    def choose_move(self,game_board):
        #first, check if board is in any of our leaves
        #if so, trim to that, else need to reset tree
        if(self.root != None):
            new_root = None
            for child in self.root.children:
                if(child.board==game_board):
                    new_root = child
            self.root = new_root

        if(self.root==None):
            print("new tree")
            self.root = Node(None,game_board,name="r")
            self.root.make_children()            
        else:
            print(self.root.name)

        self.MCTS_iter(N_iter)
        
        #for child in self.root.children:
            #print(child.name,child.ucb())

        root_after_move = self.root.max_ucb_child()
        #print(root_after_move.name)
        self.root = root_after_move
    
        if(self.root.name=="pass"):
            move = None
        else:
            move = htm_move(self.root.name)  #all child nodes have the move to get there as their name
        
        return move
        #raise Exception("dummy")
        
    def MCTS_iter(self,N):
    
        for ii in range(N):
            
            a_node = self.root
            #traverse to leaf
            while(not a_node.is_leaf()):
                a_node = a_node.max_ucb_child()

                
            if(a_node.visits == 0):
                roll_node = a_node
            else:
                if(a_node.board.game_over()):
                    roll_node = a_node
                else:
                    a_node.make_children()
                    roll_node = random.choice(a_node.children)

            value = rollout(roll_node.board)
            roll_node.backprop(value)




        
def rollout(game_board):
    rev_game = board.Reversi(copy.deepcopy(game_board),RandomPlayer("White"),RandomPlayer("Black"))

    while(not rev_game.game_over):
        rev_game.resolve_turn()

    #print(rev_game.board)
    wsc,bsc = rev_game.board.score()
    #print(wsc,bsc)
    if(wsc>bsc):
        return 1.0
    elif(bsc>wsc):
        return 0.0
    else:
        return 0.5

    


class Node():
    def __init__(self,parent,board,name=""):
        self.parent = parent
        self.board = board
        self.name=name
        self.children = []
        self.visits = 0
        self.value = 0
        if(parent != None):
            parent.children.append(self)

    def backprop(self,value):
        self.visits += 1
        #value is 1 for white win, 0 for black win, 0.5 for tie
        #if we are black, value = 1-value        
        if(self.board.turn == board.Space.BLACK):
            self.value += (value)
        elif(self.board.turn == board.Space.WHITE):
            self.value += (1-value)
            
        if(self.parent != None):
            self.parent.backprop(value)
        
    def ucb(self):
        if(self.visits == 0):
            return 100000 + random.uniform(0,1) #random number used to unbias ties
        else:
            av = self.value/self.visits
            ex = C_ex*np.sqrt( np.log(self.parent.visits)/self.visits)
            return av+ex
            
    def __repr__(self):
         return self.pp_self(0)

    def is_leaf(self):
        return self.children==[]
     
    def pp_self(self,level):
    
        pp_rep = "  "*level +  self.name + "\n"
        for child in self.children:
            
            pp_rep += child.pp_self(level+1)
            
        return pp_rep

    def max_ucb_child(self):
        if self.is_leaf():
            return None
        else:
            ucb_max = -1
            ucb_max_node = None
            
            for child in self.children:
                if(child.ucb()>ucb_max):
                    ucb_max = child.ucb()
                    ucb_max_node = child
                elif(child.ucb()==ucb_max):
                    #Really should randomly choose these
                    pass
                else:
                    pass

            return ucb_max_node

    def make_children(self):

#        if(not self.board.game_over): #no children if game is over

        legal_moves = self.board.legal_moves()

        if(len(legal_moves)==0):
            board = copy.deepcopy(self.board)
            board.place_piece(None)

            cnode = Node(self,board,name="pass")
            
            #cnode = Node(self,self.board,name="pass")
            #debug
            if(self.name=="pass"):

                raise Exception("double pass!")
            
        else:
            for move in legal_moves:
                nname = mth_move(move)

                board = copy.deepcopy(self.board)
                board.place_piece(move)

                cnode = Node(self,board,name=nname)
                #node adds itself to parent, no need to do it explicitly


N = 2000

if __name__ == "__main__":
    print("tree test")

    gb = board.Board()
    root = Node(None,gb,name="r")
    root.make_children()
    
    for ii in range(N):
        a_node = root
        #find a leaf

        while(not a_node.is_leaf()):
            a_node = a_node.max_ucb_child()

        if(a_node.visits == 0):
            roll_node = a_node
        else:
            if(a_node.board.game_over()):
                roll_node = a_node #can't expand node
            else:
                a_node.make_children()
                roll_node = random.choice(a_node.children)

        value = rollout(roll_node.board)
        roll_node.backprop(value)

    for child in root.children:
        print(child.name,child.ucb())

#    print(gb)
#    x = rollout(gb)
#    print(x)
#    #check if I need deep copy
#    print(gb)
