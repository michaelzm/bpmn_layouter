class Node:
    def __init__(self,id, label):
        self.id = id
        self.label = label
        #depth controls the x axis
        self.depth = float("-inf")
        #shift controls the y axis
        self.shift = float("inf")
        self.incoming = []
        self.outgoing = []
        self.type = []

    def add_incoming(self, incoming_element):
        self.incoming.append(incoming_element)

    def add_outgoing(self, outgoing_element):
        self.outgoing.append(outgoing_element)

    def set_type(self, type):
        self.type = type

    def set_depth(self, new_depth):
        print("changed depth from ", self.depth, " to ", new_depth)
        self.depth = new_depth

    def set_shift(self, new_shift):
        print("changed shift from ", self.depth, " to ", new_shift)
        self.shift = new_shift  

class Edge:
    def __init__(self,id, label):
        self.id = id
        self.label = label
        self.incoming = []
        self.outgoing = []
        self.direction = None
        self.type = "edge"

    def set_incoming(self, incoming_elements):
        self.incoming = [incoming_elements]

    def set_outgoing(self, outgoing_elements):
        self.outgoing = [outgoing_elements]

    def set_direction(self, direction):
        self.direction = direction