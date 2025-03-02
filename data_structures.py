class Node:
    def __init__(self,node_element):
        self.id = node_element["id"]
        self.data = node_element
        #depth controls the x axis
        self.depth = float("inf")
        #shift controls the y axis
        self.shift = float("-inf")
        self.parents = []
        self.child_nodes = []

    def set_depth(self, new_depth):
        print("changed depth from ", self.depth, " to ", new_depth)
        self.depth = new_depth

    def update_depth(self):
        min_parent_depth = min([i.depth for i in self.parents])
        print("based on all parents, min depth identified as ", min_parent_depth)
        self.depth = min_parent_depth + 1
        print("updated depth to ", self.depth)

    def set_shift(self, new_shift):
        #only change shift if the parent is closer to this nodes depth
        self.shift = new_shift
        print("shift set from ", self.shift, " to ", new_shift)
    
    def update_shift(self, elements_linked):
        #avoid counting own id that is already placed on this depth as shift
        max_shift_on_depth = len([i for i in elements_linked if elements_linked[i].depth == self.depth]) -1
        print("maximum existing shift on grid for this depth: ", max_shift_on_depth)
        depth_of_parent = self.depth -1
        print("all parents are ",self.parents)
        max_parents_shifts_on_depth = max([i.shift for i in self.parents if i.depth == depth_of_parent])
        if self.data["type"] == "flow":
            target_shift = max(max_parents_shifts_on_depth, max_shift_on_depth)
        else:
            target_shift = max_parents_shifts_on_depth
        print("target shift of ", target_shift, " based on type ", self.data["type"])
        self.set_shift(target_shift)
        print("identified shifts of parents ",max_parents_shifts_on_depth)
        
    
    def add_parent(self, parent):
        self.parents.append(parent)