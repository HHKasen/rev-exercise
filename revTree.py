

class Node():
    def __init__(self,parent,board,name=""):
        self.parent = parent
        self.board = board
        self.name=name
        self.children = []
        if(parent != None):
            parent.children.append(self)

    def __repr__(self):
         return self.pp_self(0)

    def pp_self(self,level):
    
        pp_rep = "  "*level +  self.name + "\n"
        for child in self.children:
            
            pp_rep += child.pp_self(level+1)
            
        return pp_rep
        
if __name__ == "__main__":
    print("tree test")

    root = Node(None,name="root")
    l11 = Node(root,name="l11")
    l12 = Node(root,name="l12")
    l13 = Node(root,name="l13")
    l21 = Node(l11,name="l21") 
    l23 = Node(l13,name="l23")
    print(root)
