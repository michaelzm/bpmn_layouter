import datetime

json_string_1 = "{'elements': [\n{'id': 'Event_1fgdyvq', 'type': 'startEvent', 'label': 'probable recourse detected', 'incoming': [], 'outgoing': ['Task_0iirfhd']} ,\n{'id': 'Task_0iirfhd', 'type': 'task', 'label': 'get information', 'incoming': ['Event_1fgdyvq'], 'outgoing': ['Task_0iirfhd1']} ,\n{'id': 'Task_0iirfhd1', 'type': 'task', 'label': 'check case', 'incoming': ['Task_0iirfhd'], 'outgoing': ['ExclusiveGateway_092mc05']} ,\n{'id': 'ExclusiveGateway_092mc05', 'type': 'exclusiveGateway', 'label': 'recourse possible?', 'incoming': ['Task_0iirfhd1'], 'outgoing': ['Task_02fdytg', 'Task_04aofbe']} ,\n{'id': 'Task_02fdytg', 'type': 'task', 'label': 'send request for payment', 'incoming': ['ExclusiveGateway_092mc05'], 'outgoing': ['Task_12lthpj']} ,\n{'id': 'Task_12lthpj', 'type': 'task', 'label': 'send reminder', 'incoming': ['Task_02fdytg'], 'outgoing': ['Gateway_0pkmva3']} ,\n{'id': 'Gateway_0pkmva3', 'type': 'exclusiveGateway', 'label': 'money received or deadline reached', 'incoming': ['Task_12lthpj'], 'outgoing': ['Task_1bwmf45', 'Task_1w7bb1w', 'Task_0eti3m2']} ,\n{'id': 'Task_1bwmf45', 'type': 'task', 'label': 'make booking', 'incoming': ['Gateway_0pkmva3'], 'outgoing': ['Task_0yan60f']} ,\n{'id': 'Task_0yan60f', 'type': 'task', 'label': 'close case', 'incoming': ['Task_1bwmf45'], 'outgoing': ['EndEvent_119yhl0']} ,\n{'id': 'EndEvent_119yhl0', 'type': 'endEvent', 'label': 'case closed', 'incoming': ['Task_0yan60f'], 'outgoing': []} ,\n{'id': 'Task_04aofbe', 'type': 'task', 'label': 'close case', 'incoming': ['ExclusiveGateway_092mc05'], 'outgoing': ['EndEvent_01a6rq8']} ,\n{'id': 'EndEvent_01a6rq8', 'type': 'endEvent', 'label': 'case closed', 'incoming': ['Task_04aofbe'], 'outgoing': []} ,\n{'id': 'Task_0eti3m2', 'type': 'task', 'label': 'check disagreement', 'incoming': ['Gateway_0pkmva3'], 'outgoing': ['ExclusiveGateway_0lk2nir']} ,\n{'id': 'ExclusiveGateway_0lk2nir', 'type': 'exclusiveGateway', 'label': 'disagreement valid?', 'incoming': ['Task_0eti3m2'], 'outgoing': ['Task_1qlbv5i', 'Task_1w7bb1w']} ,\n{'id': 'Task_1qlbv5i', 'type': 'task', 'label': 'close case', 'incoming': ['ExclusiveGateway_0lk2nir'], 'outgoing': ['EndEvent_0k9uozu']} ,\n{'id': 'EndEvent_0k9uozu', 'type': 'endEvent', 'label': 'case closed', 'incoming': ['Task_1qlbv5i'], 'outgoing': []} ,\n{'id': 'Task_1w7bb1w', 'type': 'task', 'label': 'hand over to collection agency', 'incoming': ['ExclusiveGateway_0lk2nir', 'Gateway_0pkmva3'], 'outgoing': ['EndEvent_0nfuudw']} ,\n{'id': 'EndEvent_0nfuudw', 'type': 'endEvent', 'label': 'case open', 'incoming': ['Task_1w7bb1w'], 'outgoing': []}\n]\n}"

xml_file_1= '''<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:omgdi="http://www.omg.org/spec/DD/20100524/DI" xmlns:omgdc="http://www.omg.org/spec/DD/20100524/DC" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="sid-38422fae-e03e-43a3-bef4-bd33b32041b2" targetNamespace="http://bpmn.io/bpmn" exporter="bpmn-js (https://demo.bpmn.io)" exporterVersion="18.1.1">
  <collaboration id="Collaboration_0dscto3">
    <participant id="Participant_1bahxc2" name="Private Person" processRef="Process_1" />
  </collaboration>
  <process id="Process_1" isExecutable="false">
    <startEvent id="StartEvent_1y45yut" name="hunger noticed">
      <outgoing>SequenceFlow_0h21x7r</outgoing>
    </startEvent>
    <task id="Task_1hcentk" name="choose recipe">
      <incoming>SequenceFlow_0h21x7r</incoming>
      <outgoing>SequenceFlow_0wnb4ke</outgoing>
    </task>
    <exclusiveGateway id="ExclusiveGateway_15hu1pt" name="desired dish?">
      <incoming>SequenceFlow_0wnb4ke</incoming>
      <outgoing>Flow_0f8fvlf</outgoing>
      <outgoing>Flow_1buytw9</outgoing>
    </exclusiveGateway>
    <task id="Activity_0utr38j" name="do not select">
      <incoming>Flow_0f8fvlf</incoming>
      <outgoing>Flow_1ovcfyt</outgoing>
    </task>
    <task id="Activity_1ps7hce" name="eat meal">
      <incoming>Flow_0j2f7e4</incoming>
      <outgoing>Flow_0l69tjn</outgoing>
    </task>
    <task id="Activity_1pguxcu" name="cook meal">
      <incoming>Flow_1buytw9</incoming>
      <outgoing>Flow_0j2f7e4</outgoing>
    </task>
    <endEvent id="Event_08s7npr" name="not hungry anymore">
      <incoming>Flow_1ovcfyt</incoming>
      <incoming>Flow_0kr7le2</incoming>
    </endEvent>
    <task id="Activity_1c1dgpx" name="be happy">
      <incoming>Flow_0l69tjn</incoming>
      <outgoing>Flow_0kr7le2</outgoing>
    </task>
    <sequenceFlow id="SequenceFlow_0h21x7r" sourceRef="StartEvent_1y45yut" targetRef="Task_1hcentk" />
    <sequenceFlow id="SequenceFlow_0wnb4ke" sourceRef="Task_1hcentk" targetRef="ExclusiveGateway_15hu1pt" />
    <sequenceFlow id="Flow_0f8fvlf" name="no" sourceRef="ExclusiveGateway_15hu1pt" targetRef="Activity_0utr38j" />
    <sequenceFlow id="Flow_1buytw9" name="yes" sourceRef="ExclusiveGateway_15hu1pt" targetRef="Activity_1pguxcu" />
    <sequenceFlow id="Flow_1ovcfyt" sourceRef="Activity_0utr38j" targetRef="Event_08s7npr" />
    <sequenceFlow id="Flow_0j2f7e4" sourceRef="Activity_1pguxcu" targetRef="Activity_1ps7hce" />
    <sequenceFlow id="Flow_0l69tjn" sourceRef="Activity_1ps7hce" targetRef="Activity_1c1dgpx" />
    <sequenceFlow id="Flow_0kr7le2" sourceRef="Activity_1c1dgpx" targetRef="Event_08s7npr" />
  </process>
  </definitions>'''


xml_file_2 ='''<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" id="Definitions_0sllhi0" targetNamespace="http://bpmn.io/schema/bpmn" exporter="bpmn-js (https://demo.bpmn.io)" exporterVersion="18.1.1">
  <bpmn:process id="Process_1a9mcyv" isExecutable="false">
    <bpmn:startEvent id="StartEvent_1ncsvoq" name="start with idea">
      <bpmn:outgoing>Flow_1rqh8d7</bpmn:outgoing>
    </bpmn:startEvent>
    <bpmn:task id="Activity_0abxoyh" name="make familiar with BPMN">
      <bpmn:incoming>Flow_1rqh8d7</bpmn:incoming>
      <bpmn:outgoing>Flow_0wb1hk4</bpmn:outgoing>
    </bpmn:task>
    <bpmn:sequenceFlow id="Flow_1rqh8d7" sourceRef="StartEvent_1ncsvoq" targetRef="Activity_0abxoyh" />
    <bpmn:task id="Activity_0haydyo" name="check github for similar projects">
      <bpmn:incoming>Flow_0wb1hk4</bpmn:incoming>
      <bpmn:outgoing>Flow_0c0dnd3</bpmn:outgoing>
    </bpmn:task>
    <bpmn:sequenceFlow id="Flow_0wb1hk4" sourceRef="Activity_0abxoyh" targetRef="Activity_0haydyo" />
    <bpmn:exclusiveGateway id="Gateway_1ksauni" name="similar projects found?">
      <bpmn:incoming>Flow_0c0dnd3</bpmn:incoming>
      <bpmn:outgoing>Flow_134bvrw</bpmn:outgoing>
      <bpmn:outgoing>Flow_1t4qaxr</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:sequenceFlow id="Flow_0c0dnd3" sourceRef="Activity_0haydyo" targetRef="Gateway_1ksauni" />
    <bpmn:task id="Activity_1c8brpz" name="code own project">
      <bpmn:incoming>Flow_134bvrw</bpmn:incoming>
      <bpmn:outgoing>Flow_1hi6vy4</bpmn:outgoing>
    </bpmn:task>
    <bpmn:sequenceFlow id="Flow_134bvrw" name="no" sourceRef="Gateway_1ksauni" targetRef="Activity_1c8brpz" />
    <bpmn:task id="Activity_1kyc9go" name="reuse existing proejct">
      <bpmn:incoming>Flow_1t4qaxr</bpmn:incoming>
      <bpmn:outgoing>Flow_07od1co</bpmn:outgoing>
    </bpmn:task>
    <bpmn:sequenceFlow id="Flow_1t4qaxr" name="yes" sourceRef="Gateway_1ksauni" targetRef="Activity_1kyc9go" />
    <bpmn:task id="Activity_00u5xrs" name="upload project progress on github">
      <bpmn:incoming>Flow_1hi6vy4</bpmn:incoming>
      <bpmn:outgoing>Flow_1fwouge</bpmn:outgoing>
    </bpmn:task>
    <bpmn:sequenceFlow id="Flow_1hi6vy4" sourceRef="Activity_1c8brpz" targetRef="Activity_00u5xrs" />
    <bpmn:endEvent id="Event_0a3c3hu" name="project done">
      <bpmn:incoming>Flow_1fwouge</bpmn:incoming>
      <bpmn:incoming>Flow_07od1co</bpmn:incoming>
    </bpmn:endEvent>
    <bpmn:sequenceFlow id="Flow_1fwouge" sourceRef="Activity_00u5xrs" targetRef="Event_0a3c3hu" />
    <bpmn:sequenceFlow id="Flow_07od1co" sourceRef="Activity_1kyc9go" targetRef="Event_0a3c3hu" />
  </bpmn:process>
</bpmn:definitions>
'''

xml_file_3 = '''<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" id="Definitions_0sllhi0" targetNamespace="http://bpmn.io/schema/bpmn" exporter="bpmn-js (https://demo.bpmn.io)" exporterVersion="18.1.1">
  <bpmn:process id="Process_1a9mcyv" isExecutable="false">
    <bpmn:startEvent id="StartEvent_1ncsvoq" name="start with idea">
      <bpmn:outgoing>Flow_1rqh8d7</bpmn:outgoing>
    </bpmn:startEvent>
    <bpmn:task id="Activity_0abxoyh" name="make familiar with BPMN">
      <bpmn:incoming>Flow_1rqh8d7</bpmn:incoming>
      <bpmn:outgoing>Flow_0wb1hk4</bpmn:outgoing>
    </bpmn:task>
    <bpmn:sequenceFlow id="Flow_1rqh8d7" sourceRef="StartEvent_1ncsvoq" targetRef="Activity_0abxoyh" />
    <bpmn:task id="Activity_0haydyo" name="check github for similar projects">
      <bpmn:incoming>Flow_0wb1hk4</bpmn:incoming>
      <bpmn:outgoing>Flow_0c0dnd3</bpmn:outgoing>
    </bpmn:task>
    <bpmn:sequenceFlow id="Flow_0wb1hk4" sourceRef="Activity_0abxoyh" targetRef="Activity_0haydyo" />
    <bpmn:exclusiveGateway id="Gateway_1ksauni" name="similar projects found?">
      <bpmn:incoming>Flow_0c0dnd3</bpmn:incoming>
      <bpmn:outgoing>Flow_134bvrw</bpmn:outgoing>
      <bpmn:outgoing>Flow_1t4qaxr</bpmn:outgoing>
      <bpmn:outgoing>Flow_1uqtfg6</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:sequenceFlow id="Flow_0c0dnd3" sourceRef="Activity_0haydyo" targetRef="Gateway_1ksauni" />
    <bpmn:task id="Activity_1c8brpz" name="code own project">
      <bpmn:incoming>Flow_134bvrw</bpmn:incoming>
      <bpmn:outgoing>Flow_1hi6vy4</bpmn:outgoing>
    </bpmn:task>
    <bpmn:sequenceFlow id="Flow_134bvrw" name="no" sourceRef="Gateway_1ksauni" targetRef="Activity_1c8brpz" />
    <bpmn:task id="Activity_1kyc9go" name="reuse existing proejct">
      <bpmn:incoming>Flow_1t4qaxr</bpmn:incoming>
      <bpmn:outgoing>Flow_07od1co</bpmn:outgoing>
    </bpmn:task>
    <bpmn:sequenceFlow id="Flow_1t4qaxr" name="yes" sourceRef="Gateway_1ksauni" targetRef="Activity_1kyc9go" />
    <bpmn:task id="Activity_00u5xrs" name="upload project progress on github">
      <bpmn:incoming>Flow_1hi6vy4</bpmn:incoming>
      <bpmn:outgoing>Flow_1fwouge</bpmn:outgoing>
    </bpmn:task>
    <bpmn:sequenceFlow id="Flow_1hi6vy4" sourceRef="Activity_1c8brpz" targetRef="Activity_00u5xrs" />
    <bpmn:endEvent id="Event_0a3c3hu" name="project done">
      <bpmn:incoming>Flow_1fwouge</bpmn:incoming>
      <bpmn:incoming>Flow_07od1co</bpmn:incoming>
      <bpmn:incoming>Flow_13bfl99</bpmn:incoming>
    </bpmn:endEvent>
    <bpmn:sequenceFlow id="Flow_1fwouge" sourceRef="Activity_00u5xrs" targetRef="Event_0a3c3hu" />
    <bpmn:sequenceFlow id="Flow_07od1co" sourceRef="Activity_1kyc9go" targetRef="Event_0a3c3hu" />
    <bpmn:task id="Activity_17ps7sz" name="maybe">
      <bpmn:incoming>Flow_1uqtfg6</bpmn:incoming>
      <bpmn:outgoing>Flow_13bfl99</bpmn:outgoing>
    </bpmn:task>
    <bpmn:sequenceFlow id="Flow_1uqtfg6" sourceRef="Gateway_1ksauni" targetRef="Activity_17ps7sz" />
    <bpmn:sequenceFlow id="Flow_13bfl99" sourceRef="Activity_17ps7sz" targetRef="Event_0a3c3hu" />
  </bpmn:process>
</bpmn:definitions>
'''


json_string_2 = '''{"elements": [
{"id": "Event_0j8g4tq", "type": "startEvent", "label": "detect drop in loading", "incoming": [], "outgoing": ["Task_0iirfhd"]} ,
{"id": "Task_0iirfhd", "type": "task", "label": "trigger assessment", "incoming": ["Event_0j8g4tq"], "outgoing": ["ExclusiveGateway_092mc05"]} ,
{"id": "ExclusiveGateway_092mc05", "type": "exclusiveGateway", "label": "sub-bottleneck blocking loading?", "incoming": ["Task_0iirfhd"], "outgoing": ["Task_02fdytg", "Task_04aofbe"]} ,
{"id": "Task_02fdytg", "type": "task", "label": "check with BackEnd OPC RP", "incoming": ["ExclusiveGateway_092mc05"], "outgoing": ["ExclusiveGateway_0lk2nir"]} ,
{"id": "ExclusiveGateway_0lk2nir", "type": "exclusiveGateway", "label": "can increase sub-bottleneck demands capacity?", "incoming": ["Task_02fdytg"], "outgoing": ["Task_1qlbv5i", "Task_1w7bb1w"]} ,
{"id": "Task_1qlbv5i", "type": "task", "label": "update bottleneck capacity", "incoming": ["ExclusiveGateway_0lk2nir"], "outgoing": ["Task_1bwmf45"]} ,
{"id": "Task_1bwmf45", "type": "task", "label": "assess cut rate for bottlenecks", "incoming": ["Task_1qlbv5i"], "outgoing": ["Gateway_0pkmva3"]} ,
{"id": "Task_04aofbe", "type": "task", "label": "check demands, semi-constraints, and front-end chip shortages", "incoming": ["ExclusiveGateway_092mc05"], "outgoing": ["ExclusiveGateway_0lk2nir2"]} ,
{"id": "ExclusiveGateway_0lk2nir2", "type": "exclusiveGateway", "label": "chip shortages from front end?", "incoming": ["Task_04aofbe"], "outgoing": ["Task_1w7bb1w2", "Task_1qlbv5i2"]} ,
{"id": "Task_1w7bb1w2", "type": "task", "label": "ask SCP to check FrontEnd chip supply", "incoming": ["ExclusiveGateway_0lk2nir2"], "outgoing": ["Gateway_0pkmva3"]} ,
{"id": "Task_1qlbv5i2", "type": "task", "label": "assess Cap line considering non-production days and holidays", "incoming": ["ExclusiveGateway_0lk2nir2"], "outgoing": ["Gateway_0pkmva3"]} ,
{"id": "Task_1w7bb1w", "type": "task", "label": "manual data pull and capacity determination", "incoming": ["ExclusiveGateway_0lk2nir"], "outgoing": ["Gateway_0pkmva3"]} ,
{"id": "Gateway_0pkmva3", "type": "exclusiveGateway", "label": "", "incoming": ["Task_1bwmf45", "Task_1w7bb1w2", "Task_1qlbv5i2", "Task_1w7bb1w"], "outgoing": ["Task_0yan60f", "Task_0eti3m2"]} ,
{"id": "Task_0yan60f", "type": "task", "label": "send email or call meeting with SCP", "incoming": ["Gateway_0pkmva3"], "outgoing": ["Task_0eti3m2"]} ,
{"id": "Task_0eti3m2", "type": "task", "label": "collaborate with SCP and discuss adjustments", "incoming": ["Gateway_0pkmva3", "Task_0yan60f"], "outgoing": ["ExclusiveGateway_0lk2nir3"]} ,
{"id": "ExclusiveGateway_0lk2nir3", "type": "exclusiveGateway", "label": "SCP or SCM want to maintain days?", "incoming": ["Task_0eti3m2"], "outgoing": ["Task_1qlbv5i3", "Task_1w7bb1w3"]} ,
{"id": "Task_1qlbv5i3", "type": "task", "label": "provide research and ETA with regular follow-ups", "incoming": ["ExclusiveGateway_0lk2nir3"], "outgoing": ["EndEvent_0k9uozu"]} ,
{"id": "Task_1w7bb1w3", "type": "task", "label": "monitor and update bottleneck capacity", "incoming": ["ExclusiveGateway_0lk2nir3"], "outgoing": ["EndEvent_0k9uozu"]} ,
{"id": "EndEvent_0k9uozu", "type": "endEvent", "label": "BackEnd Cap process complete", "incoming": ["Task_1qlbv5i3", "Task_1w7bb1w3"], "outgoing": []}
]
}'''