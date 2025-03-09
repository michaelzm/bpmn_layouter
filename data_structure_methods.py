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
        print("\n flow generation")
        print(elem_id)
        if "flow" in elements_linked[elem_id].data["type"]:
            #incoming edge
            incoming_edges = find_edge_to_target_connection(elements_linked, lookup_placement, elem_id, "incoming")
            outgoing_edges = find_edge_to_target_connection(elements_linked, lookup_placement, elem_id, "outgoing")
            elements_linked[elem_id].data["label"]
            print(elem_id, incoming_edges, outgoing_edges)
            #add width and height
            elements_linked[elem_id].position = incoming_edges + outgoing_edges
    
    return elements_linked, id_depth_mapping

def find_longest_simple_path(start_node):
    """
    Returns the longest simple path (as a list of nodes) beginning at start_node.
    A 'simple path' does not revisit any node (avoids cycles).
    """
    best_path = []
    
    def dfs(current, path, visited):
        nonlocal best_path
        
        # Mark current node as visited for this path
        visited.add(current)
        path.append(current)
        
        # Explore all children that are not yet visited
        advanced = False
        for child in current.child_nodes:
            if child not in visited:
                advanced = True
                dfs(child, path, visited)
                
        # If we didn't move forward (no unvisited children), it's a dead end => check path length
        if not advanced:
            if len(path) > len(best_path):
                best_path = path[:]
        
        # Backtrack
        path.pop()
        visited.remove(current)
    
    dfs(start_node, [], set())
    return best_path

def get_longest_path_from_start(nodes_dict):
    """
    Finds the node with depth == 0, then returns the list of Node objects
    representing the longest simple path starting from that node.
    """
    # Identify the start node (depth == 0)
    start_node = None
    for node_id, node in nodes_dict.items():
        if node.depth == 0:
            start_node = node
            break
    
    if not start_node:
        raise ValueError("No start node (depth=0) found.")
    
    # Compute the longest simple path
    longest_path = find_longest_simple_path(start_node)
    return longest_path


def find_longest_path_single_abort(start_node, end_nodes):
    """
    Finds the longest simple path (no repeated nodes) starting from `start_node`, 
    stopping when we encounter any node that is either in `end_nodes` or has no children.
    
    In other words, each path can contain at most one 'abort' node 
    (either in end_nodes or a node with zero children).
    Once we hit an abort node, we record that path length, do not continue from that node,
    but backtrack to explore other possible branches in the graph.
    
    :param start_node:  the Node from which to begin searching
    :param end_nodes:   a set of Node objects considered "end"/"abort" nodes
    :return:            a list of Node objects corresponding to the single longest path found
    """
    best_path = []

    def dfs(current, path, visited):
        nonlocal best_path

        visited.add(current)
        path.append(current)

        # Check if current is an "abort" node: in end_nodes or no children
        if (current in end_nodes) or (not current.child_nodes):
            # Record this path if it's the longest so far
            if len(path) > len(best_path):
                best_path = path[:]
            # Do NOT continue from this node -- end the current path
        else:
            # If not an abort node, explore children that are not yet visited
            for child in current.child_nodes:
                if child not in visited:
                    dfs(child, path, visited)

        # Backtrack
        path.pop()
        visited.remove(current)

    dfs(start_node, [], set())
    return best_path


def get_longest_path_single_abort(
    all_nodes_dict,
    start_node_id,
    end_node_ids
):
    """
    Helper function to:
      1) Convert input IDs to Node objects
      2) Call find_longest_path_single_abort 
      3) Return the result
    """
    start_node = all_nodes_dict[start_node_id]
    
    # Convert ID -> Node for each 'end' node
    end_nodes = {all_nodes_dict[eid] for eid in end_node_ids if eid in all_nodes_dict}

    longest_path = find_longest_path_single_abort(start_node, end_nodes)
    return longest_path

def find_max_gateway_in_list(elem_list):
    print("calculating gateway based on ")
    max_idx_gateway = -1
    for idx, i in enumerate(elem_list):
        print(i.data)
        if i.data["type"] == "exclusiveGateway" and not i.data["processed"]:
            max_idx_gateway = idx

    #set the processed gateway to cold so it will not be returned a second time
    elem_list[max_idx_gateway].data["processed"] = True
    print("higehst gateway identified as ",max_idx_gateway, elem_list[max_idx_gateway].data["label"])
    return max_idx_gateway

def calculate_forward_looking_shift(elements_as_nodes, starting_elem_id, ending_elems):
    '''
    Calcualte the forwad looking shift in a given window.
    Only shfits already placed within the minimum and maximum depth should count to not explode the grid
    '''
    minimum_depth = elements_as_nodes[starting_elem_id].depth
    maximum_depth = ending_elems[-1].depth - 1
    if maximum_depth > 1023:
        maximum_depth = minimum_depth + len(ending_elems)
    highest_shift = 0
    for elem in elements_as_nodes:
        if elements_as_nodes[elem].depth >= minimum_depth and elements_as_nodes[elem].depth <= maximum_depth:
            if elements_as_nodes[elem].shift > highest_shift:
                print("identified ", elements_as_nodes[elem].id, elements_as_nodes[elem].data["label"], " as highest shift")
                highest_shift = elements_as_nodes[elem].shift
    print("highest shift between depths ", minimum_depth, maximum_depth, " as ", highest_shift)
    return highest_shift

def dump_positions(elements_as_nodes):
    print("\n dump postions ----")
    for elem in elements_as_nodes:
        print(elements_as_nodes[elem].id , elements_as_nodes[elem].data["label"], elements_as_nodes[elem].depth, elements_as_nodes[elem].shift)
    print("\n dump postions ----")

def dump_data(elements):
    print("\n dump data ----")
    for elem in elements:
        print(elem.id , elem.data["label"], elem.data)
    print("\n dump data ----")

def init_shift_and_depth(elements_as_nodes):
    #identify base path and set to depth i, shift = 0
    base_path = get_longest_path_from_start(elements_as_nodes)
    starting_shift = base_path[0].shift
    print("starting shift", starting_shift)
    for elem in base_path:
        elem.update_depth()
        elem.set_shift(starting_shift)
        elem.data["processed"] = False
    print("longest path as ", [i.id for i in base_path])
    all_paths_visited = False
    rec_count = 0
    while not all_paths_visited:
        all_paths_visited = check_gateway(elements_as_nodes, base_path, rec_count)

def check_gateway(elements_as_nodes, base_path, rec_count):
    rec_count = rec_count +1 
    print("in nested recursion of ", rec_count)
    dump_positions(elements_as_nodes)
    all_single_paths_visited = False
    while not all_single_paths_visited:
        current_path = base_path
        print("current path set as ",current_path )
        print("path as labels" , [i.data["label"] for i in current_path])
        highest_idx = find_max_gateway_in_list(current_path)
        if highest_idx > 0:
            all_paths_checked = False
            current_path = current_path[highest_idx:]
            all_outgoing_paths = current_path[0].child_nodes
            print("for current path all out ", all_outgoing_paths)
            outgoing_length = len(all_outgoing_paths)
            outgoing_iter = 1
            ending_elems_buffer = []
            while not all_paths_checked:
                print("\nsub path analysis")
                print("subpath is ", current_path)
                print("subpath as labels" , [i.data["label"] for i in current_path])
                #returns the longest subset path, starting from idx1 since idx0 is the exclusive gateway
                starting_elem = current_path[0].id
                ending_elems = [i.id for i in current_path[1:]]
                ending_elems_buffer = ending_elems_buffer + ending_elems
                print("ending elements buffer set to ", ending_elems_buffer)
                print("ending elements identified as ", [elements_as_nodes[i].data["label"] for i in ending_elems_buffer])
                longest_full_path = get_longest_path_single_abort(elements_as_nodes, starting_elem, ending_elems_buffer)
                longest_subset_path = longest_full_path[1:]
                print("longest subset paths", longest_subset_path)
                print("length of paths found ", len(longest_subset_path))
                print("longest subset path as ", [i.id for i in longest_subset_path])
                print("longest subset path as labels" , [i.data["label"] for i in longest_subset_path])
                highest_relevant_ending_elem = longest_subset_path[-1]
                print("relevant ending elem", highest_relevant_ending_elem, highest_relevant_ending_elem.id, highest_relevant_ending_elem.data["label"])
                placement_shift = calculate_forward_looking_shift(elements_as_nodes, starting_elem, longest_subset_path) + 1
                #dump_positions(elements_as_nodes)
                for elem in longest_subset_path:
                    if elem.id not in ending_elems_buffer:
                        print("updaing elem", elem.data["label"])
                        elem.update_depth()
                        elem.set_shift(placement_shift)
                        elem.data["processed"] = False
                highest_idx = find_max_gateway_in_list(longest_subset_path)
                print("new highest idx meaning gate found at ", highest_idx)
                outgoing_iter += 1
                print("outgoing iter", outgoing_iter, outgoing_length)

                #means no gateway found, proceed as usual
                if highest_idx == -1:
                    if outgoing_iter >= outgoing_length:
                        print("all subpaths checked, no later gateway, returning analysis to main path")
                        all_paths_checked = True
                        current_path = base_path
                    else:
                        #outgoing_iter < outgoing_length:
                        #means there is another path but the current path has no other gateway
                        current_path = longest_full_path
                        #add the elements of the current path to all known ending elements to find the next path
                        ending_elems_buffer = ending_elems_buffer + [i.id for i in longest_subset_path]
                else:
                    #means there is a gateway that requires placement, TOOD implement
                    #TODO work with stack to make new base path and return to old base bath once all gateways processed
                    print("there is a gateway in subpath, setting current path to longest subpath")
                    all_gateways_checked_rec = False
                    print("staring recursion with the same function")
                    new_base_path = longest_subset_path
                    print("resetting processed status so gateways can be found again leaving all other cold")
                    new_base_path[highest_idx].data["processed"] = False
                    new_base_path[highest_idx].data["iteration"] = rec_count + 1
                    while not all_gateways_checked_rec:
                        all_gateways_checked_rec = check_gateway(elements_as_nodes, new_base_path, rec_count)
                    print("recursion finished, storing the elements of this path so they will not be reused and going back to main path call")
                    for elem in new_base_path:
                        ending_elems_buffer.append(elem.id)
                    print("final dump")
                    dump_data(new_base_path)
            print("all linked paths of this gateway successfully checked")
        else:
            #means base path has no gateways if in first iteration
            print("all gateways checked, aborting path finding")
            return True


##alterantive implementation
#requires base path id list -> list of start element longest path ids
from collections import deque

def topological_sort(nodes_dict):
    """
    Returns a list of nodes in topological order,
    ignoring any nodes that are stuck in cycles.
    """
    # Build an in-degree map
    in_degree = {}
    for node in nodes_dict.values():
        in_degree[node] = len(node.parents)
    
    # Collect all nodes that have in_degree = 0 to start
    queue = deque(n for n, deg in in_degree.items() if deg == 0)
    sorted_nodes = []
    
    while queue:
        current = queue.popleft()
        sorted_nodes.append(current)
        
        # Decrease in-degree of each child. If it hits zero, enqueue child.
        for child in current.child_nodes:
            in_degree[child] -= 1
            if in_degree[child] == 0:
                queue.append(child)
    
    return sorted_nodes


##fallback solution
def assign_depth_and_shift(elements_as_nodes, base_path_ids):
    """
    Assigns each Node in 'elements_as_nodes' a unique (depth, shift).
    
    :param elements_as_nodes: dict of { node_id: Node }.
    :param base_path_ids:     list of node IDs that form the "main" path.
                              These will be placed at shift=0, in increasing depth.
    
    After completion, each Node object has .depth and .shift set.
    
    NOTE: Nodes that are part of cycles and never reach in-degree=0 will be skipped
          in the topological ordering. If you have cycles you want to lay out,
          you'll need a different or more advanced approach.
    """
    # 1) Reset all nodes' depth and shift
    for node in elements_as_nodes.values():
        node.depth = float("inf")
        node.shift = float("inf")
    
    # 2) Place the base path at shift=0
    #    e.g. if base_path_ids = ["Event_0j8g4tq", "Task_0iirfhd", ...]
    used_positions = {}  # Maps depth -> set of used shifts
    
    for i, node_id in enumerate(base_path_ids):
        node = elements_as_nodes[node_id]
        node.depth = i
        node.shift = 0
        used_positions.setdefault(i, set()).add(0)
    
    # 3) Get a topological ordering of all nodes (ignores cycles)
    sorted_nodes = topological_sort(elements_as_nodes)
    
    # 4) Assign (depth, shift) to nodes not on the base path, in topo order
    for node in sorted_nodes:
        # If node already has depth set (meaning it's in the base path), skip
        if node.depth < float("inf"):
            continue
        
        # (a) Determine depth = 1 + max of all parent depths
        if not node.parents:
            # No parents => it can be placed at depth=0 (or next free column).
            # This is somewhat arbitrary if it's truly "floating."
            node.depth = 0
        else:
            # Filter out any parent that still has depth=inf (unassigned),
            # in case they were skipped because of cycles or the parent's not assigned yet
            valid_parent_depths = [p.depth for p in node.parents if p.depth < float("inf")]
            if valid_parent_depths:
                node.depth = max(valid_parent_depths) + 1
            else:
                node.depth = 0
        
        # (b) Find a suitable shift
        if not node.parents:
            # No parents => start from shift=0
            candidate_shift = 0
        else:
            # Inherit the minimum parent's shift as a starting point, for consistency
            valid_parent_shifts = [p.shift for p in node.parents if p.shift > float("-inf")]
            candidate_shift = min(valid_parent_shifts) if valid_parent_shifts else 0
        
        used_at_this_depth = used_positions.setdefault(node.depth, set())
        while candidate_shift in used_at_this_depth:
            candidate_shift += 1
        
        node.shift = candidate_shift
        used_at_this_depth.add(candidate_shift)