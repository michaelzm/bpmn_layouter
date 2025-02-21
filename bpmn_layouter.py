from bpmn_to_json_parser import bpmn_to_json, json_to_flattened_dict
from data_structures import Node
from data_structure_methods import parse_tree, init_element_positions
from placement_config import lookup_placement
from xml_position_appender import xml_position_appender

class BpmnLayout:
    def __init__(self):
        pass

    def generate_bpmn_layout(self, xml_input_file, xml_output_name):
        flattened_json = bpmn_to_json(xml_data=xml_input_file)
        flattened_dict = json_to_flattened_dict(flattened_json)
        elements_as_nodes = {}
        for element_id in flattened_dict:
            elements_as_nodes[element_id] = Node(flattened_dict[element_id])

        elements_linked = parse_tree(elements_linked=elements_as_nodes)
        elements_linked = init_element_positions(lookup_placement, elements_linked)

        xml_position_appender(elements_linked, xml_input_file, xml_output_name)