from copy import deepcopy

def find_start_node_id(elements_not_in_tree):
    for elem in elements_not_in_tree:
        print(elem)
        if "type" in elements_not_in_tree[elem].data and elements_not_in_tree[elem].data["type"] == "startEvent":
            print("start_element_found", elem)
            return  elem

def parse_tree(elements_not_in_tree):
    print("init tree and set top node to start node")
    top_node = elements_not_in_tree[find_start_node_id(elements_not_in_tree)]
    top_node.set_depth(0)

    fully_tracked_nodes = []
    #start with top node
    untracked_nodes = [top_node]
    while len(untracked_nodes) > 0:
        print(untracked_nodes, " open to be tracked")
        current_node = untracked_nodes[0]
        print("current node set to ", current_node.id)
        #pessimistic approach, current node always has next node in data
        all_childs_tracked = False
        while not all_childs_tracked:
            child_nodes = [i.id for i in current_node.child_nodes]
            if len(child_nodes) < len(current_node.data["outgoing"]):
                print("captured child nodes ",child_nodes)
                print("existing outgoing nodes ",current_node.data["outgoing"])
                untracked_childs = [i for i in current_node.data["outgoing"] if i not in child_nodes]
                print("untracked childs", untracked_childs)
                child_node = elements_not_in_tree[untracked_childs[0]]
                child_node.add_parent(current_node)
                child_node.set_depth(current_node.depth+1)
                max_shift_on_depth = len([i for i in elements_not_in_tree if elements_not_in_tree[i].depth == current_node.depth+1]) -1
                new_shift = max(current_node.shift, max_shift_on_depth)
                child_node.set_shift(new_shift)

                current_node.child_nodes.append(child_node)
                untracked_nodes.append(child_node)
                print("missing child")
            else:
                print("all child nodes are tracked")
                all_childs_tracked = True
                untracked_nodes.pop(0)

    #elements not in tree now have linked information
    return elements_not_in_tree

def find_preceeding_element_position(lookup_placement, elements_not_in_tree, elem_id):
    print("finding preceeding element max width plus x")
    incoming_flows = elements_not_in_tree[elem_id].data["incoming"]
    preceeding_elements = []
    if len(incoming_flows) == 0:
        return lookup_placement["initial-spacing-left"]
    else:
        for inc_flow_id in incoming_flows:
            preceeding_elements += elements_not_in_tree[inc_flow_id].data["incoming"]
    #find max x + width
    x_plus_width = []
    print("all preceeding elements ", preceeding_elements)
    for prec_elem in preceeding_elements:
        x_plus_width.append(elements_not_in_tree[prec_elem].position["x"] + elements_not_in_tree[prec_elem].position["width"])
    print(preceeding_elements)
    return max(x_plus_width)

def find_edge_to_target_connection(elements_not_in_tree, lookup_placement, edge_id, direction):
    #simple case, same shift:
    # incoming defines starting point
    # outgoing defines end point
    print("finding preceeding element max width plus x")
    target_element_id = elements_not_in_tree[edge_id].data[direction][0]
    target_element = elements_not_in_tree[target_element_id]
    
    target_edge_shift = target_element.shift
    #shift, that is level, of edge
    source_edege_shift = elements_not_in_tree[edge_id].shift
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

def init_element_positions(lookup_placement, elements_not_in_tree):
    #for positioning, traverse based on depth
    id_depth_mapping = {}
    for elem_id in elements_not_in_tree:
        depth = elements_not_in_tree[elem_id].depth
        if depth not in id_depth_mapping:
            id_depth_mapping[depth] = [elem_id]
        else:
            id_depth_mapping[depth].append(elem_id) 
    print("finished depth mapping ", id_depth_mapping)
    for depth in sorted(id_depth_mapping.keys()): 
        for elem_id in id_depth_mapping[depth]:
            print(elem_id)
            if "flow" not in elements_not_in_tree[elem_id].data["type"]:
                #add width and height
                elements_not_in_tree[elem_id].position = deepcopy(lookup_placement[elements_not_in_tree[elem_id].data["type"]])
                #grab preceeding element
                previous_element_x = find_preceeding_element_position(lookup_placement, elements_not_in_tree, elem_id)
                print("previous element placed at ", previous_element_x)
                elements_not_in_tree[elem_id].position["x"] = previous_element_x + lookup_placement["spacing-left"]
                half_height_elem = elements_not_in_tree[elem_id].position["height"] / 2
                elements_not_in_tree[elem_id].position["y"] = elements_not_in_tree[elem_id].shift * lookup_placement["y-line-spacing"] - half_height_elem + lookup_placement["initial-spacing-top"]
                print("current element placement at ", elem_id, elements_not_in_tree[elem_id].position)
    ## init flow positions
    for elem_id in elements_not_in_tree:
        print(elem_id)
        if "flow" in elements_not_in_tree[elem_id].data["type"]:
            #incoming edge
            incoming_edges = find_edge_to_target_connection(elements_not_in_tree, lookup_placement, elem_id, "incoming")
            outgoing_edges = find_edge_to_target_connection(elements_not_in_tree, lookup_placement, elem_id, "outgoing")
            #add width and height
            elements_not_in_tree[elem_id].position = incoming_edges + outgoing_edges
    
    return elements_not_in_tree