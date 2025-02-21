def xml_position_appender(elements_linked, input_xml, output_name):
    xml_fragments = '\n<bpmndi:BPMNDiagram id="BpmnDiagram_1">'
    xml_fragments += '\n<bpmndi:BPMNPlane id="BpmnPlane_1" bpmnElement="Collaboration_0dscto3">'
    xml_fragments += '\n<bpmndi:BPMNShape id="Participant_1bahxc2_di" bpmnElement="Participant_1bahxc2" isHorizontal="true">'
    xml_fragments += '\n<dc:Bounds x="50" y="50" width="1400" height="250" />'
    xml_fragments += '\n<bpmndi:BPMNLabel />'
    xml_fragments += '\n</bpmndi:BPMNShape>'

    for elem_id in elements_linked:
        print(elem_id)
        type = elements_linked[elem_id].data["type"]
        if type == "flow":
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

    with open(f"{output_name}.xml", "w") as file:
        file.write(new_xml)