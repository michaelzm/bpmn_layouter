from copy import deepcopy
from placement_config import lookup_placement

def find_start_node_id(elements_linked):
    for elem in elements_linked:
        print(elem)
        if "type" in elements_linked[elem].data and elements_linked[elem].data["type"] == "startEvent":
            print("start_element_found", elem)
            return  elem

def parse_tree(elements_linked):
    print("init tree and set top node to start node")
    top_node = elements_linked[find_start_node_id(elements_linked)]
    top_node.shift = 0
    top_node.depth = 0
    print("top node identified as ", top_node.data)
    #init top node with depth = 0
    # depth = "x"
    # shift = "y"
    top_node.set_depth(0)
    #start with top node
    untracked_nodes = [top_node]
    while len(untracked_nodes) > 0:
        print("\n")
        print("all untracked parent nodes ", [i.id for i in untracked_nodes])
        print(len(untracked_nodes), " open to be tracked")
        ## sort based on lowest shift 
        current_node = sorted(untracked_nodes, key=lambda node: node.shift)[0]
        print("current node set to ", current_node.id)
        #pessimistic approach, current node always has next node in data
        all_childs_tracked = False
        while not all_childs_tracked:

            child_nodes = [child.id  for child in current_node.child_nodes]
            if len(child_nodes) < len(current_node.data["outgoing"]):
                print("captured child nodes ",child_nodes)
                untracked_childs = [i for i in current_node.data["outgoing"] if i not in child_nodes]
                print("untracked childs", untracked_childs)
                child_node = elements_linked[untracked_childs[0]]
                print("child node for op", child_node.id)
                print("depth of current node realtive to current child node ",current_node.depth, " ", child_node.depth)
                child_node.add_parent(current_node)
                child_node.update_depth()
                
                # shift / y is set based on parent node shift and max elements at depth registered
                # for every iteration, a element in the "tree" gets udpated with the according shift. 
                # As the elements on the same depth are added ("one element -> one shift") iteratively
                # new nodes get assigned the next higher shift as well
                child_node.update_shift(elements_linked)
                
                #print("try setting shift to max of current node and placed nodes as ",new_shift)
                print(f"adding the child {child_node.id} to all untracked nodes")
                current_node.child_nodes.append(child_node)
                untracked_nodes.append(child_node)
            else:
                print("all child nodes are tracked")
                all_childs_tracked = True
                print("stack of untracked parent nodes before remove", [i.id for i in untracked_nodes])
                print("removing current node id after being processed: ",current_node.id)
                untracked_nodes.remove(current_node)
                print("stack of untracked parent nodes after remove", [i.id for i in untracked_nodes])


    #elements not in tree now have linked information
    return elements_linked

def find_preceeding_element_position(lookup_placement, elements_linked, elem_id):
    print("finding preceeding element max width plus x")
    incoming_flows = elements_linked[elem_id].data["incoming"]
    preceeding_elements = []
    if len(incoming_flows) == 0:
        return lookup_placement["initial-spacing-left"]
    else:
        for inc_flow_id in incoming_flows:
            preceeding_elements += elements_linked[inc_flow_id].data["incoming"]
    #find max x + width
    x_plus_width = []
    print("all preceeding elements ", preceeding_elements)
    for prec_elem in preceeding_elements:
        x_plus_width.append(elements_linked[prec_elem].position["x"] + elements_linked[prec_elem].position["width"])
    print(preceeding_elements)
    return max(x_plus_width)

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
        
        if direction == "incoming":
            edge_connections.append(connect_point_connection)
            edge_connections.append(break_point_connection)
        else:
            edge_connections.append(break_point_connection)
            edge_connections.append(connect_point_connection)

    return edge_connections

def init_element_positions(elements_linked):
    #for positioning, traverse based on depth
    id_depth_mapping = {}
    for elem_id in elements_linked:
        depth = elements_linked[elem_id].depth
        if depth not in id_depth_mapping:
            id_depth_mapping[depth] = [elem_id]
        else:
            id_depth_mapping[depth].append(elem_id)
    id_depth_mapping = dict(sorted(id_depth_mapping.items()))

    print("finished depth mapping ", id_depth_mapping)
    for depth in id_depth_mapping.keys():
        print("\nsettings positions for elements on depth ", depth)
        for elem_id in id_depth_mapping[depth]:
            print(elem_id)
            if "flow" not in elements_linked[elem_id].data["type"]:
                #add width and height
                elements_linked[elem_id].position = deepcopy(lookup_placement[elements_linked[elem_id].data["type"]])
                elements_linked[elem_id].position["x"] = depth*lookup_placement["x-line-spacing"] + lookup_placement["spacing-left"]
                half_height_elem = elements_linked[elem_id].position["height"] / 2
                elements_linked[elem_id].position["y"] = elements_linked[elem_id].shift * lookup_placement["y-line-spacing"] - half_height_elem + lookup_placement["initial-spacing-top"]
                print("current element placement at ", elem_id, elements_linked[elem_id].position)
    ## init flow positions
    for elem_id in elements_linked:
        print(elem_id)
        if "flow" in elements_linked[elem_id].data["type"]:
            #incoming edge
            incoming_edges = find_edge_to_target_connection(elements_linked, lookup_placement, elem_id, "incoming")
            outgoing_edges = find_edge_to_target_connection(elements_linked, lookup_placement, elem_id, "outgoing")
            #add width and height
            elements_linked[elem_id].position = incoming_edges + outgoing_edges
    
    return elements_linked, id_depth_mapping