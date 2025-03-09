class Node:
    def __init__(self,node_element):
        self.id = node_element["id"]
        self.data = node_element
        #depth controls the x axis
        self.depth = float("-inf")
        #shift controls the y axis
        self.shift = float("inf")
        self.parents = []
        self.child_nodes = []

    def set_depth(self, new_depth):
        print("changed depth from ", self.depth, " to ", new_depth)
        self.depth = new_depth

    def update_depth(self):
        if self.parents == []:
            self.depth = 0
            return True
        min_parent_depth = max([i.depth for i in self.parents])
        self.depth = min_parent_depth + 1
        return True

    def set_shift(self, new_shift):
        #only change shift if the parent is closer to this nodes depth
        #only allow to set shifts that are smaller than current
        if new_shift < self.shift:
            self.shift = new_shift  
    
    def add_parent(self, parent):
        self.parents.append(parent)