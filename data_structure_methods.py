from copy import deepcopy
from placement_config import lookup_placement
from data_structures import Node, Edge
import json
import numpy as np
import pydot
import re


def find_start_node_id(elements_linked):
    for elem in elements_linked:
        print(elem)
        if "type" in elements_linked[elem].data and elements_linked[elem].data["type"] == "startEvent":
            print("start_element_found", elem)
            return  elem
        
def assign_shift_and_depth(parsed_json):
    print(parsed_json)
    
    # Create a pydot graph with desired attributes
    graph = pydot.Dot(graph_type="digraph", 
                      rankdir="LR",  # horizontal layout
                      splines="line", 
                      overlap="false")
    id_to_label_dict = {}
    elements_as_data_struc = {}
    # Add nodes
    for n in parsed_json["elements"]:
        if n["id"] not in id_to_label_dict:
            id_to_label_dict[n["id"]] = n["label"]
        node = pydot.Node(n["id"], label=n["label"])
        graph.add_node(node)
        new_node = Node(n["id"], n["label"])
        new_node.set_type(n["type"])
        elements_as_data_struc[n["id"]] = new_node
    


    # Add edges
    for f in parsed_json["flows"]:
        print("parsing out flow ",f)
        print(f)
        from_elem = f["incoming"][0]
        to_elem = f["outgoing"][0]
        edge = pydot.Edge(from_elem, to_elem)
        new_edge = Edge(f["id"], f["label"])
        if f["id"] not in id_to_label_dict:
            id_to_label_dict[f["id"]] = f["label"]
        new_edge.set_incoming(from_elem)
        new_edge.set_outgoing(to_elem)

        ##add incoming and outgoing to the actual nodes as well
        elements_as_data_struc[to_elem].add_incoming(f["id"])
        elements_as_data_struc[from_elem].add_outgoing(f["id"])

        elements_as_data_struc[f["id"]] = new_edge
        #todo direction later
        graph.add_edge(edge)

    print("extracted labels ", id_to_label_dict)
    print("cleaning labels ")
    # Remove special characters from each string value
    id_to_label_dict = {k: re.sub(r'[^\w\s]', '', v) if isinstance(v, str) else v for k, v in id_to_label_dict.items()}
    print("cleaned labels ", id_to_label_dict)

    #batch update all nodes and edges with cleaned labels
    for e in elements_as_data_struc:
        converted_label = id_to_label_dict[e]
        elements_as_data_struc[e].label = converted_label


    # Get the plain text output to compute positions.
    plain_text = graph.create_plain().decode("utf-8")
    print("Graphviz Plain Output:")
    print(plain_text)

    # Parse the plain output for node positions.
    node_positions = {}
    for line in plain_text.splitlines():
        parts = line.split()
        if parts and parts[0] == "node":
            # Expected format:
            # node <name> <x> <y> <width> <height> <label> ...
            name = parts[1]
            x = float(parts[2])
            y = float(parts[3])
            node_positions[name] = (x, y)

    print("Node Positions:")
    for name, pos in node_positions.items():
        print(f"Node {name}, label {id_to_label_dict[name]}: Position {pos}")

    # Optionally, write the graph to a PNG file.
    # Write the graph to a PNG file

    all_x = []
    all_y = []
    print("node positions wo processed ", node_positions)
    for e in node_positions:
        all_x.append(node_positions[e][0])
        all_y.append(node_positions[e][1])
    all_x = sorted(np.unique(all_x))
    all_y = sorted(np.unique(all_y))

    float_mapping_x = {}
    for i, x in enumerate(all_x):
        float_mapping_x[x] = i

    max_y = len(all_y) -1
    float_mapping_y = {}
    for i, y in enumerate(all_y):
        float_mapping_y[y] = abs(i-max_y)

    node_positions_mapped = {}
    print("all x", all_x)
    print("all y", all_y)
    for e in node_positions:
        mapped_x = float_mapping_x[node_positions[e][0]]
        mapped_y = float_mapping_y[node_positions[e][1]]
        node_positions_mapped[e] = (mapped_x, mapped_y)

    print(node_positions_mapped)
    graph.write_png(f'outputs/graph_output_pydot_{i}.png')
    
    # set node strucutre depth and shift based on graph layout extracted value
    for e in elements_as_data_struc:
        if e in node_positions_mapped:
            elements_as_data_struc[e].set_depth(node_positions_mapped[e][0])
            elements_as_data_struc[e].set_shift(node_positions_mapped[e][1])
    print(elements_as_data_struc)
    dump_positions(elements_as_data_struc)

    for e in elements_as_data_struc:
        if elements_as_data_struc[e].type == "edge":
            from_elem = elements_as_data_struc[e].incoming[0]
            to_elem = elements_as_data_struc[e].outgoing[0]

            from_depth = elements_as_data_struc[from_elem].depth
            to_depth = elements_as_data_struc[to_elem].depth

            if from_depth > to_depth:
                elements_as_data_struc[e].set_direction("RL")
            else:
                elements_as_data_struc[e].set_direction("LR")
    return elements_as_data_struc

def find_edge_to_target_connection_rev(elements_linked, lookup_placement, edge_id):
    print("processing edge ", edge_id)
    direction = elements_linked[edge_id].direction
    print("direction found as ", direction)
    target_element_id = elements_linked[edge_id].outgoing[0]
    
    target_element = elements_linked[target_element_id]
    
    target_edge_shift = target_element.shift
    print("target is ", target_element.label, " with shift ", target_edge_shift)


    source_element_id = elements_linked[edge_id].incoming[0]
    source_element = elements_linked[source_element_id]
    
    source_edge_shift = source_element.shift
    print("source is ", source_element.label, " with shift ", source_edge_shift)
    #shift, that is level, of edge
    edge_connections = []

    shift_delta = target_edge_shift - source_edge_shift
    print("detected shift delta of ",shift_delta)

    # case same shift = straight connection
    if shift_delta == 0:
        print("same shift")
        ##we move from left to right so we connect on left side of incmonig elem
        if direction == "LR":
            #start with first break point of the starting element
            breakpoint1_x = source_element.position["x"] + source_element.position["width"]
            breakpoint1_y = source_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"]
            edge1 = {"x": breakpoint1_x, "y":breakpoint1_y}
            
            breakpoint2_x = target_element.position["x"]
            breakpoint2_y = target_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"]
            edge2 = {"x": breakpoint2_x, "y":breakpoint2_y}
        else:
            #we have flowing back information, right to left
            breakpoint1_x = source_element.position["x"]
            breakpoint1_y = source_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"] + source_element.position["height"] * 0.25
            edge1 = {"x": breakpoint1_x, "y":breakpoint1_y}

            breakpoint2_x = target_element.position["x"] + target_element.position["width"]
            breakpoint2_y = source_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"] + source_element.position["height"] * 0.25
            edge2 = {"x": breakpoint2_x, "y":breakpoint2_y}

    #we break off up or down, left or right
    else:
        print("different shift")
        #less than zero means we go up
        if shift_delta < 0:
            #lr and rl matters as the edges will conenct at 0.5 height and 0.25 height each
            if direction == "LR":
                #branch off gateway at top and bottom
                if source_element.type == "exclusiveGateway":
                    #we go up
                    breakpoint1_x = source_element.position["x"] + source_element.position["width"] * 0.5

                    #start at top mid
                    breakpoint1_y = source_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"] -  source_element.position["height"] * 0.5
                    edge1 = {"x": breakpoint1_x, "y":breakpoint1_y}
                    
                    ## we stop on 90 degree angle when moving up relative to the target shift
                    breakpoint2_x = source_element.position["x"] + source_element.position["width"] * 0.5
                    breakpoint2_y = target_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"]
                    edge2 = {"x": breakpoint2_x, "y":breakpoint2_y}

                    #third edge connets from this breakpoint to the left side
                    breakpoint3_x = target_element.position["x"]
                    breakpoint3_y = target_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"]
                    edge3 = {"x": breakpoint3_x, "y":breakpoint3_y}
                #all other branch off to the left
                else:
                    #we go up
                    breakpoint1_x = source_element.position["x"] + source_element.position["width"]

                    #start at top mid
                    breakpoint1_y = source_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"]
                    edge1 = {"x": breakpoint1_x, "y":breakpoint1_y}
                    
                    ## we stop on 90 degree angle when moving up relative to the target shift
                    breakpoint2_x = target_element.position["x"] + target_element.position["width"] * 0.25
                    breakpoint2_y = source_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"]
                    edge2 = {"x": breakpoint2_x, "y":breakpoint2_y}

                    #third edge connets from this breakpoint to the left side
                    breakpoint3_x = target_element.position["x"] + target_element.position["width"] * 0.25
                    breakpoint3_y = target_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"] + target_element.position["height"] * 0.5
                    edge3 = {"x": breakpoint3_x, "y":breakpoint3_y}

            else:
                if source_element.type == "exclusiveGateway":
                    #means we go right to left but we move up
                    #we go up
                    breakpoint1_x = source_element.position["x"] + source_element.position["width"] * 0.5
                    #start at top mid
                    breakpoint1_y = source_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"] +  source_element.position["height"] * 0.5
                    edge1 = {"x": breakpoint1_x, "y":breakpoint1_y}
                    
                    ## we stop on 90 degree angle when moving up relative to the target shift
                    breakpoint2_x = source_element.position["x"] + source_element.position["width"] * 0.5
                    breakpoint2_y = target_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"] +  target_element.position["height"] * 0.5
                    edge2 = {"x": breakpoint2_x, "y":breakpoint2_y}

                    #third edge connets from this breakpoint to the left side
                    breakpoint3_x = target_element.position["x"]
                    breakpoint3_y = target_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"] +  target_element.position["height"] * 0.5
                    edge3 = {"x": breakpoint3_x, "y":breakpoint3_y}
                else:
                    #we go up
                    breakpoint1_x = source_element.position["x"]

                    #start at top mid
                    breakpoint1_y = source_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"] + source_element.position["height"] * 0.25
                    edge1 = {"x": breakpoint1_x, "y":breakpoint1_y}
                    
                    ## we stop on 90 degree angle when moving up relative to the target shift, connect on right side
                    breakpoint2_x = target_element.position["x"] + target_element.position["width"] * 0.75
                    breakpoint2_y = source_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"] + source_element.position["height"] * 0.25
                    edge2 = {"x": breakpoint2_x, "y":breakpoint2_y}

                    #third edge connets from this breakpoint to the left side
                    breakpoint3_x = target_element.position["x"] + target_element.position["width"] * 0.75
                    breakpoint3_y = target_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"] + target_element.position["height"] * 0.5
                    edge3 = {"x": breakpoint3_x, "y":breakpoint3_y}
        else:
            #means we go down, so we connect first breakpoint at bottom
            #lr and rl matters as the edges will conenct at 0.5 height and 0.25 height each
            if direction == "LR":
                if source_element.type == "exclusiveGateway":
                    #we go up
                    breakpoint1_x = source_element.position["x"] + source_element.position["width"] * 0.5

                    #start at top mid
                    breakpoint1_y = source_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"] +  source_element.position["height"] * 0.5
                    edge1 = {"x": breakpoint1_x, "y":breakpoint1_y}
                    
                    ## we stop on 90 degree angle when moving down relative to the target shift
                    breakpoint2_x = source_element.position["x"] + source_element.position["width"] * 0.5
                    breakpoint2_y = target_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"]
                    edge2 = {"x": breakpoint2_x, "y":breakpoint2_y}

                    #third edge connets from this breakpoint to the left side
                    breakpoint3_x = target_element.position["x"]
                    breakpoint3_y = target_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"]
                    edge3 = {"x": breakpoint3_x, "y":breakpoint3_y}
                else:
                    #we go down
                    breakpoint1_x = source_element.position["x"] + source_element.position["width"]
                    breakpoint1_y = source_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"]
                    edge1 = {"x": breakpoint1_x, "y":breakpoint1_y}
                    
                    ## we stop on 90 degree angle when moving down relative to the target shift
                    breakpoint2_x = target_element.position["x"] + target_element.position["width"] * 0.25
                    breakpoint2_y = source_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"]
                    edge2 = {"x": breakpoint2_x, "y":breakpoint2_y}

                    #third edge connets from this breakpoint to the left side
                    breakpoint3_x = target_element.position["x"] + target_element.position["width"] * 0.25
                    breakpoint3_y = target_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"] - target_element.position["height"] * 0.5
                    edge3 = {"x": breakpoint3_x, "y":breakpoint3_y}
            else:
                if source_element.type == "exclusiveGateway":
                    #means we go right to left but we move down
                    #we go up
                    breakpoint1_x = source_element.position["x"] + source_element.position["width"] * 0.5
                    #start at top mid
                    breakpoint1_y = source_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"] - source_element.position["height"] * 0.5
                    edge1 = {"x": breakpoint1_x, "y":breakpoint1_y}
                    
                    ## we stop on 90 degree angle when moving up relative to the target shift
                    breakpoint2_x = source_element.position["x"] + source_element.position["width"] * 0.5
                    breakpoint2_y = target_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"] +  target_element.position["height"] * 0.5
                    edge2 = {"x": breakpoint2_x, "y":breakpoint2_y}

                    #third edge connets from this breakpoint to the left side
                    breakpoint3_x = target_element.position["x"]
                    breakpoint3_y = target_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"] +  target_element.position["height"] * 0.5
                    edge3 = {"x": breakpoint3_x, "y":breakpoint3_y}
                else:
                    #means we go right to left but we move down
                    breakpoint1_x = source_element.position["x"]
                    #start at top mid
                    breakpoint1_y = source_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"] - source_element.position["height"] * 0.25
                    edge1 = {"x": breakpoint1_x, "y":breakpoint1_y}
                    
                    ## we stop on 90 degree angle when moving up relative to the target shift
                    breakpoint2_x = target_element.position["x"] + target_element.position["width"]
                    breakpoint2_y = source_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"] -  source_element.position["height"] * 0.25
                    edge2 = {"x": breakpoint2_x, "y":breakpoint2_y}

                    #third edge connets from this breakpoint to the left side
                    breakpoint3_x = target_element.position["x"] + target_element.position["width"]
                    breakpoint3_y = target_edge_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"] -  target_element.position["height"] * 0.25
                    edge3 = {"x": breakpoint3_x, "y":breakpoint3_y}

    edge_connections.append(edge1)
    edge_connections.append(edge2)
    if shift_delta != 0:
        edge_connections.append(edge3)
    print("calculated edge connectinos ", edge_connections)
    return edge_connections

def find_edge_to_target_connection(elements_linked, lookup_placement, edge_id, direction):
    #simple case, same shift:
    # incoming defines starting point
    # outgoing defines end point
    print("finding preceeding element max width plus x")
    target_element_id = elements_linked[edge_id].data[direction][0]
    target_element = elements_linked[target_element_id]
    
    target_edge_shift = target_element.shift
    #shift, that is level, of edge
    source_edege_shift = elements_linked[edge_id].shift
    #if edge and target are on same shift, use single connector
    edge_connections = []
    if source_edege_shift == target_edge_shift:
        print("same shift")
        single_edge_x = target_element.position["x"]
        if direction == "incoming":
            single_edge_x += target_element.position["width"]
        single_edge_y = source_edege_shift*lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"]
        single_edge_connection = {"x":single_edge_x, "y": single_edge_y}
        edge_connections.append(single_edge_connection)
    else:
        if direction == "incoming":
            # we define break point
            print("different shift")
            #in that case we need to treat them based on the target direction
            
            # this case already implies that we will branch down or up
                #we take the y line of the target as y baseline
            y_connect_point = target_element.shift * lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"]
            x_baseline = target_element.position["x"] + target_element.position["width"]
            if target_edge_shift < source_edege_shift:
                print("do someting ")
                #means we go up, hence we add half of height to baseline
                y_connect_point = y_connect_point
            else:
                print("do something")
                #means we go down, hence we remove half of height from baseline
                y_connect_point = y_connect_point
            
            y_break_point = source_edege_shift * lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"]
            connect_point_connection = {"x": x_baseline, "y":y_connect_point}
            break_point_connection = {"x": x_baseline, "y": y_break_point}
            edge_connections.append(connect_point_connection)
            edge_connections.append(break_point_connection)
        #else equals to outgoing
        else:
            # we define break point
            print("different shift")
            #in that case we need to treat them based on the target direction
            
            # this case already implies that we will branch down or up
                #we take the y line of the target as y baseline
            y_connect_point = target_element.shift * lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"]
            x_baseline = target_element.position["x"] + target_element.position["width"] * 0.5
            if target_edge_shift < source_edege_shift:
                print("do someting ")
                #means we go up, hence we add half of height to baseline
                y_connect_point += target_element.position["height"] * 0.5
            else:
                print("do something")
                #means we go down, hence we remove half of height from baseline
                y_connect_point -= target_element.position["height"] * 0.5
            
            y_break_point = source_edege_shift * lookup_placement["y-line-spacing"] + lookup_placement["initial-spacing-top"]
            connect_point_connection = {"x": x_baseline, "y":y_connect_point}
            break_point_connection = {"x": x_baseline, "y": y_break_point}
            edge_connections.append(break_point_connection)
            edge_connections.append(connect_point_connection)

    return edge_connections

def dump_positions(elements_as_nodes):
    print("\n dump postions ----")
    for elem in elements_as_nodes:
        if elements_as_nodes[elem].type != "edge":
            print(elements_as_nodes[elem].id , elements_as_nodes[elem].label, elements_as_nodes[elem].depth, elements_as_nodes[elem].shift)
    print("\n dump postions ----")

def dump_data(elements):
    print("\n dump data ----")
    for elem in elements:
        print(elem.id , elem.data["label"], elem.data)
    print("\n dump data ----")

def init_element_positions(elements_linked):
    #for positioning, traverse based on depth

    for elem_id in elements_linked:
        print(elem_id)
        if elements_linked[elem_id].type != "edge":
            #add width and height
            elements_linked[elem_id].position = deepcopy(lookup_placement[elements_linked[elem_id].type])
            elements_linked[elem_id].position["x"] = elements_linked[elem_id].depth * lookup_placement["x-line-spacing"] + lookup_placement["spacing-left"]
            half_height_elem = elements_linked[elem_id].position["height"] / 2
            elements_linked[elem_id].position["y"] = elements_linked[elem_id].shift * lookup_placement["y-line-spacing"] - half_height_elem + lookup_placement["initial-spacing-top"]
            print("current element placement at ", elem_id, elements_linked[elem_id].position)

    ## init flow positions
    for elem_id in elements_linked:
        print("\n flow generation")
        print(elem_id)
        if elements_linked[elem_id].type == "edge":
            calculated_edges = find_edge_to_target_connection_rev(elements_linked, lookup_placement, elem_id)
            
            elements_linked[elem_id].position = calculated_edges
            pass
    return elements_linked
