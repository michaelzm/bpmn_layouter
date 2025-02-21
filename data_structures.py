class Node:
    def __init__(self,node_element):
        self.id = node_element["id"]
        self.data = node_element
        #depth controls the x axis
        self.depth = 0
        #shift controls the y axis
        self.shift = 0
        self.parents = []
        self.child_nodes = []

    def set_depth(self, new_depth):
        print("try setting depth on node to ", new_depth)
        if self.depth != None:
            if self.depth < new_depth:
                self.depth = new_depth
                print("success setting depth")
            else:
                print("depth on node already set to ", self.depth)
    
    def set_shift(self, new_shift):
        print("setting shift to ", new_shift)
        self.shift = new_shift

    def add_parent(self, parent):
        self.parents.append(parent)