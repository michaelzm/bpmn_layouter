import xml.etree.ElementTree as ET
import json
import os

def bpmn_to_json(xml_data):
    ns = {'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL'}
    root = ET.fromstring(xml_data)
    process = root.find('bpmn:process', ns)

    elements_data = []
    flows_data = []

    # Collect elements (startEvent, endEvent, task, gateway, etc.)
    for elem in process:
        tag = elem.tag.split('}')[1]
        if tag != 'sequenceFlow':
            elem_id = elem.attrib.get('id', '')
            elem_type = tag
            label = elem.attrib.get('name', '')
            incoming = [inc.text for inc in elem.findall('bpmn:incoming', ns)]
            outgoing = [out.text for out in elem.findall('bpmn:outgoing', ns)]
            elements_data.append({
                "id": elem_id,
                "type": elem_type,
                "label": label,
                "incoming": incoming,
                "outgoing": outgoing,
                "condition": None
            })
        else:
            flow_id = elem.attrib.get('id', '')
            source = elem.attrib.get('sourceRef', '')
            target = elem.attrib.get('targetRef', '')
            condition = elem.attrib.get('name', '')
            flows_data.append({
                "id": flow_id,
                "type":"flow",
                "label":f"Flow{source}-{target}",
                "incoming": [source],
                "outgoing": [target],
                "condition": condition
            })

    return {"elements": elements_data, "flows": flows_data}

def generate_flows_based_on_elements(parsed_json):
    flows_created = []
    for elem in parsed_json["elements"]:
        #means there are still elements that are not mapped to flows
        current_elem_id = elem["id"]
        while len(elem["outgoing"]) > 0:
            elem_id_to_convert = elem["outgoing"][0]
            elem["outgoing"].remove(elem_id_to_convert)
            new_flow = {
                'id': '',
                'type': 'flow',
                'label': '',
                'incoming': [],
                'outgoing': [],
            }
            new_flow["id"] = f"flow_{current_elem_id}_{elem_id_to_convert}"
            new_flow["incoming"].append(current_elem_id)
            new_flow["outgoing"].append(elem_id_to_convert)
            elem["outgoing_flows"].append(new_flow["id"])
            flows_created.append(new_flow)
            for elem_target in parsed_json["elements"]:
                if elem_target["id"] == elem_id_to_convert:
                    if current_elem_id in elem_target:
                        elem_target["incoming"].remove(current_elem_id)
                    elem_target["incoming_flows"].append(new_flow["id"])

    for elem in parsed_json["elements"]:
        elem["incoming"] = elem["incoming_flows"]
        elem["outgoing"] = elem["outgoing_flows"]
        del elem["outgoing_flows"], elem["incoming_flows"]
    parsed_json["flows"] = flows_created
    return parsed_json

def json_to_flattened_dict(flattened_json):
    flattened_dict = {}
    for elem in flattened_json["elements"]:
        flattened_dict[elem["id"]] = elem
    for flow in flattened_json["flows"]:
        flattened_dict[flow["id"]] = flow
    return flattened_dict

def generate_top_bpmn_xml(nodes):
    """
    nodes: a dictionary like:
        {
          "Event_1fgdyvq": <Node object>,
          "Task_0iirfhd": <Node object>,
          ...
        }
    where each node.data might look like:
        {
          "id": "Event_1fgdyvq",
          "type": "startEvent",
          "label": "probable recourse detected",
          "incoming": [],
          "outgoing": ["flow_Event_1fgdyvq_Task_0iirfhd"]
        }

    Returns a string of BPMN XML.
    """

    # -- 1) Collect all flows separately for generating <bpmn:sequenceFlow> tags later --

    # -- 2) Start constructing the BPMN XML output --
    xml_output = []
    xml_output.append('<?xml version="1.0" encoding="UTF-8"?>')
    xml_output.append('<bpmn:definitions '
                      'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                      'xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" '
                      'xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" '
                      'xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" '
                      'xmlns:di="http://www.omg.org/spec/DD/20100524/DI" '
                      'id="Definitions_0sllhi0" '
                      'targetNamespace="http://bpmn.io/schema/bpmn" '
                      'exporter="bpmn-js (https://demo.bpmn.io)" '
                      'exporterVersion="18.1.1">')
    xml_output.append('  <bpmn:process id="Process_1a9mcyv" isExecutable="false">')

    # -- 3) Emit one block for each node based on its 'type' --
    for node_key, node_obj in nodes.items():
        node_id = node_obj.id
        node_type = node_obj.type
        label = node_obj.label
        incoming_flows = node_obj.incoming
        outgoing_flows = node_obj.outgoing

        # Decide which BPMN element tag to use
        if node_type == "startEvent":
            # Example of a start event
            xml_output.append(f'    <bpmn:startEvent id="{node_id}" name="{label}">')
            for inc in incoming_flows:
                xml_output.append(f'      <bpmn:incoming>{inc}</bpmn:incoming>')
            for out in outgoing_flows:
                xml_output.append(f'      <bpmn:outgoing>{out}</bpmn:outgoing>')
            xml_output.append('    </bpmn:startEvent>')

        elif node_type == "endEvent":
            # Example of an end event
            xml_output.append(f'    <bpmn:endEvent id="{node_id}" name="{label}">')
            for inc in incoming_flows:
                xml_output.append(f'      <bpmn:incoming>{inc}</bpmn:incoming>')
            for out in outgoing_flows:
                xml_output.append(f'      <bpmn:outgoing>{out}</bpmn:outgoing>')
            xml_output.append('    </bpmn:endEvent>')

        elif node_type == "exclusiveGateway":
            # Exclusive gateway
            xml_output.append(f'    <bpmn:exclusiveGateway id="{node_id}" name="{label}">')
            for inc in incoming_flows:
                xml_output.append(f'      <bpmn:incoming>{inc}</bpmn:incoming>')
            for out in outgoing_flows:
                xml_output.append(f'      <bpmn:outgoing>{out}</bpmn:outgoing>')
            xml_output.append('    </bpmn:exclusiveGateway>')

        elif "TASK" in node_type.upper():
            # By default, treat as a task (e.g., userTask, scriptTask, or any generic activity).
            # You could extend this with other BPMN types if needed.
            xml_output.append(f'    <bpmn:task id="{node_id}" name="{label}">')
            for inc in incoming_flows:
                xml_output.append(f'      <bpmn:incoming>{inc}</bpmn:incoming>')
            for out in outgoing_flows:
                xml_output.append(f'      <bpmn:outgoing>{out}</bpmn:outgoing>')
            xml_output.append('    </bpmn:task>')
        
        elif node_type == "edge":
            if len(incoming_flows) > 0:
                xml_output.append(f'    <bpmn:sequenceFlow id="{node_id}" name="{label}" sourceRef="{incoming_flows[0]}" targetRef="{outgoing_flows[0]}" />')
        
    # -- 5) Close the process and definitions --
    xml_output.append('  </bpmn:process>')
    xml_output.append('</bpmn:definitions>')

    # Return as a single string
    return "\n".join(xml_output)


def xml_position_appender(elements_linked, input_xml, output_name):
    xml_fragments = '\n<bpmndi:BPMNDiagram id="BpmnDiagram_1">'
    xml_fragments += '\n<bpmndi:BPMNPlane id="BpmnPlane_1" bpmnElement="Collaboration_0dscto3">'
    xml_fragments += '\n<bpmndi:BPMNShape id="Participant_1bahxc2_di" bpmnElement="Participant_1bahxc2" isHorizontal="true">'
    xml_fragments += '\n<dc:Bounds x="50" y="50" width="1400" height="250" />'
    xml_fragments += '\n<bpmndi:BPMNLabel />'
    xml_fragments += '\n</bpmndi:BPMNShape>'

    for elem_id in elements_linked:
        print(elem_id)
        type = elements_linked[elem_id].type
        if type == "edge":
            xml_fragments += f'<bpmndi:BPMNEdge id="{elem_id}_di" bpmnElement="{elem_id}">\n'
            for breakpoint in elements_linked[elem_id].position:
                print(breakpoint)
                xml_fragments += f'<di:waypoint x="{breakpoint["x"]}" y="{breakpoint["y"]}"/>'
            xml_fragments += f'</bpmndi:BPMNEdge>\n'
        else:
            position = elements_linked[elem_id].position
            xml_fragments += (
                f'<bpmndi:BPMNShape id="{elem_id}_di" bpmnElement="{elem_id}">\n'
                f'  <dc:Bounds x="{position["x"]}" y="{position["y"]}" width="{position["width"]}" height="{position["height"]}" />\n'
                f'  <bpmndi:BPMNLabel>\n'
                f'  </bpmndi:BPMNLabel>\n'
                f'</bpmndi:BPMNShape>\n'
            )
    xml_fragments += '</bpmndi:BPMNPlane>\n'
    xml_fragments += '</bpmndi:BPMNDiagram>'
    insertion_point = input_xml.find("</bpmn:process>")
    if insertion_point != -1:
        print("inserting to xml file")
        new_xml = (input_xml[:insertion_point + len("</bpmn:process>")] +
                xml_fragments +
                input_xml[insertion_point + len("</bpmn:process>"):])
    print("outputting file as ",output_name)

    file_name = f"outputs/{output_name}.xml"
    if os.path.exists(file_name):
        os.remove(file_name)
    
    with open(file_name, "w") as file:
        file.write(new_xml)