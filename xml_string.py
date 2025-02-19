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