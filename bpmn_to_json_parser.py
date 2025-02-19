import xml.etree.ElementTree as ET
import json

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

def json_to_flattened_dict(flattened_json):
    flattened_dict = {}
    for elem in flattened_json["elements"]:
        flattened_dict[elem["id"]] = elem
    for flow in flattened_json["flows"]:
        flattened_dict[flow["id"]] = flow
    return flattened_dict